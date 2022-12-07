# -*- coding: UTF-8 -*-
from datetime import (
    datetime,
)
from wsgiref.util import (
    FileWrapper,
)

import docx
from api.const import (
    ANALYSIS_ACT_MODIFIED,
    ANALYSIS_ACT_SIMPLE,
    APPLICANT_IN_CERTIFICATE_WL_IS_L,
    APPLICANT_IN_CERTIFICATE_WL_IS_NOT_L,
    CHANGES,
    DAY_FORMAT,
    FORMAT,
    MANUFACTURER_LOCATION_AND_WORK_LOCATION,
    MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION,
    MANUFACTURER_NAME_AND_LOCATION,
    MANUFACTURING_COMPANIES,
    MANUFACTURING_COMPANIES_LOCATION,
    MANUFACTURING_COMPANIES_WORK_LOCATION,
    MONTHS,
    NUMBER_BY_DATE,
    PROTOCOL_DATE_NUMBER_FORM,
    PROTOCOL_FINAL_MODIFIED,
    PROTOCOL_FINAL_MODIFIED_PLURAL,
    PROTOCOL_FINAL_SIMPLE,
    PROTOCOL_FINAL_SIMPLE_PLURAL,
    PROTOCOL_ORDER_FIELD_NAME,
    PROTOCOL_START_SIMPLE_PLURAL,
    TEMP_FILE_NAME, PROTOCOL_START_MODIFIED_PLURAL, PROTOCOL_START_SIMPLE,
    PROTOCOL_START_MODIFIED,
)
from api.utils import (
    obj_checker,
)
from django.db.models import (
    Count,
    Q,
)
from django.http import (
    HttpResponse,
)
from django.utils.encoding import (
    escape_uri_path,
)
from documents.models import (
    Pattern,
    Protocol,
    Work,
)
from docx import (
    Document,
)
from rest_framework import (
    status,
)
from rest_framework.response import (
    Response,
)


def date_format(date: datetime.date) -> str:
    return date.strftime(FORMAT)


def doc_splitter(text: str) -> list:
    return text.replace('\r', '').split('\n')


def is_qms(text: str):
    return 'СМК' in text or '9001' in text or 'анализа состояния' in text


class FillInDocument:

    def __init__(self, work: Work, template: str):
        self.work: Work = work
        self.template: str = template
        self.template_rus: str = CHANGES.get(self.template)

    def get_changes(self):
        return getattr(self, self.template)()

    def get_document_date(self):
        return getattr(self.work, f'{self.template}_date')

    def get_docs_with_application_without_report(self):
        docs_with_application_without_report: list = []
        for value in self.work.application.docs_with_application:
            if "протокол" not in value and "Протокол" not in value:
                docs_with_application_without_report.append(value)
        return docs_with_application_without_report

    def get_manufacturing_companies(self):
        manufacturing_companies = []
        if self.work.application.manufacturing_companies.exists():
            manufacturing_companies.append(MANUFACTURING_COMPANIES)
            for company in self.work.application.manufacturing_companies.all():
                manufacturing_companies.append(company.name)
                manufacturing_companies.append(
                    MANUFACTURING_COMPANIES_LOCATION.format(
                        location=company.location
                    )
                )
                manufacturing_companies.append(
                    MANUFACTURING_COMPANIES_WORK_LOCATION.format(
                        work_location=company.work_location
                    )
                )
        else:
            manufacturing_companies.append('-')
        return ''.join(manufacturing_companies)

    def get_tn_ved_keys(self):
        return ', '.join(
            str(obj.name)
            for obj in self.work.application.tn_ved_keys.all()
        )

    def get_manufacturer_location(self):
        manufacturer_data = {
            'location': self.work.application.manufacturer.location,
            'work_location': self.work.application.manufacturer.work_location
        }
        if (
                manufacturer_data.get('location')
                in (manufacturer_data.get('work_location'),)
        ):
            return (
                MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION.format(
                    **manufacturer_data
                )
            )
        return (
            MANUFACTURER_LOCATION_AND_WORK_LOCATION.format(
                **manufacturer_data
            )
        )

    def get_report_evidentiary_and_analise_act(
            self,
            simple=True,
            backspace=True
    ):
        report_evidentiary = self.get_certificate_protocols_with_description(
            simple, backspace
        ) or ''
        analysis_act = ''
        if self.work.act_analysis_production_date:
            if simple:
                analysis_act = ANALYSIS_ACT_SIMPLE.format(
                    number=self.work.number,
                    date=date_format(self.work.act_analysis_production_date)
                )
            else:
                analysis_act = ANALYSIS_ACT_MODIFIED.format(
                    number=self.work.number,
                    date=date_format(self.work.act_analysis_production_date)
                )

        return f'{report_evidentiary}{analysis_act}'

    def get_certificate_protocols_with_description(
            self,
            simple: bool = True,
            backspace: bool = True
    ) -> str:
        protocols = []
        provided_protocols = Protocol.objects.filter(
            Q(works=self.work)
            or Q(applications=self.work.application)
        ).all()
        body_count = (
            Protocol.objects.filter(
                Q(works=self.work)
                or Q(applications=self.work.application)
            ).values(
                PROTOCOL_ORDER_FIELD_NAME
            ).order_by(
                PROTOCOL_ORDER_FIELD_NAME
            ).annotate(
                count=Count(PROTOCOL_ORDER_FIELD_NAME)
            ).all()
        )
        counter = {
            data.get(PROTOCOL_ORDER_FIELD_NAME): data.get('count')
            for data in body_count
        }
        body_protocol_count = 0
        line_break = ''
        if backspace:
            line_break = '\n'
        first_protocol = True
        for protocol in provided_protocols:
            first_char = 'П' if first_protocol or backspace else 'п'
            if body_protocol_count == 0:
                if counter.get(protocol.body_certificate) > 1:
                    if simple:
                        protocols.append(
                            first_char + PROTOCOL_START_SIMPLE_PLURAL
                        )
                    else:
                        protocols.append(
                            first_char + PROTOCOL_START_MODIFIED_PLURAL
                        )
                else:
                    if simple:
                        protocols.append(
                            first_char + PROTOCOL_START_SIMPLE
                        )
                    else:
                        protocols.append(
                            first_char + PROTOCOL_START_MODIFIED
                        )
            body_protocol_count += 1
            first_protocol = False
            protocol_num_and_date = {
                'number': protocol.number,
                'date': date_format(protocol.date)
            }
            if body_protocol_count != counter.get(protocol.body_certificate):
                protocols.append(
                    PROTOCOL_DATE_NUMBER_FORM.format(
                        **protocol_num_and_date
                    ) + ','
                )
            else:
                protocols.append(
                    PROTOCOL_DATE_NUMBER_FORM.format(**protocol_num_and_date)
                )
                body = {
                    'body_name': protocol.body_name,
                    'body_certificate': protocol.body_certificate
                }
                if counter.get(protocol.body_certificate) > 1:
                    if simple:
                        protocols.append(
                            PROTOCOL_FINAL_SIMPLE_PLURAL.format(**body)
                            + line_break
                        )
                    else:
                        protocols.append(
                            PROTOCOL_FINAL_MODIFIED_PLURAL.format(**body)
                            + line_break
                        )

                else:
                    if simple:
                        protocols.append(
                            PROTOCOL_FINAL_SIMPLE.format(**body)
                            + line_break
                        )
                    else:
                        protocols.append(
                            PROTOCOL_FINAL_MODIFIED.format(**body)
                            + line_break
                        )
                body_protocol_count = 0
        return ' '.join(protocols)

    def document_creator(self):
        temp_filename = self.form_fill()
        filename = escape_uri_path(f'{self.template_rus} {self.work.name}')
        if temp_filename:
            with open(temp_filename, 'rb') as worddoc:
                return HttpResponse(
                    FileWrapper(
                        worddoc
                    ),
                    headers={
                        'Content-Type':
                            'application/vnd.openxmlformats-officedocument'
                            '.wordprocessingml.document',
                        'Content-Disposition':
                            f'attachment; filename="{filename}.docx"',
                    }
                )
        return Response(
            data={'detail': 'Нет подходящего шаблона'},
            status=status.HTTP_404_NOT_FOUND
        )

    def form_fill(self) -> Document:
        pattern = Pattern.objects.filter(
            date_issue__lte=self.get_document_date(),
            name=self.template
        ).first()
        if pattern:
            doc = docx.Document(pattern.file)
            obj_checker(doc, self.get_changes())
            filename = escape_uri_path(
                TEMP_FILE_NAME.format(name=self.work.name)
            )
            doc.save(filename)
            return filename
        return None

    def conclusion_application_analyze(self) -> dict:
        return {
            'conclusion_application_analyze_num_with_dt':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(
                        self.work.conclusion_application_analyze_date
                    )
                ),
            'application_num_with_dt':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(self.work.date)
                ),
            'applicant_name':
                self.work.application.applicant.name,
            'prod_name':
                self.work.application.prod_name,
            'manufacturer_name':
                self.work.application.manufacturer.name,
            'tn_ved_key':
                self.get_tn_ved_keys(),
            'docs_with_application':
                self.work.application.docs_with_application.replace('\r', ''),
            'number_of_requirenment':
                f'{self.work.application.standard.name}'
                f'\n{self.work.application.reglament.name}',
            'conclusion_application_analyze_expert':
                self.work.application_analyze_expert.name
        }

    def application_decision(self) -> dict:
        recognition_evidentiary_materials = []
        qms_certificate_evidentiary = []
        for value in doc_splitter(self.work.application.docs_with_application):
            if is_qms(value):
                qms_certificate_evidentiary.append(value)
            if ('Протокол' in value
                    or 'протокол' in value
                    or 'СМК' in value
                    or '9001' in value
                    or 'анализа состояния' in value):
                recognition_evidentiary_materials.append(value)
        recognition_evidentiary_materials = '\n'.join(
            recognition_evidentiary_materials)
        return {
            'application_num':
                self.work.number,
            'certification_decision_day':
                DAY_FORMAT.format(
                    date=self.work.application_decision_date.day
                ),
            'certification_decision_month':
                MONTHS[self.work.application_decision_date.month - 1],
            'certification_decision_year':
                f'{self.work.application_decision_date.year}г.',
            'application_dt':
                date_format(self.work.date),
            'applicant_name':
                self.work.application.applicant.name,
            'prod_name':
                self.work.application.prod_name,
            'manufacturer_name':
                self.work.application.manufacturer.name,
            'reglament':
                self.work.application.reglament.name,
            'certification_schem':
                self.work.application.schem.name,
            'recognition_as_evidentiary_materials':
                recognition_evidentiary_materials,
            'production_status_analysis':
                'В соответствии с п.33 ТР ТС 018/2011 провести на основании'
                ' анализа:\n'
                + '\n'.join(qms_certificate_evidentiary),
            'agreement_num_and_dt':
                NUMBER_BY_DATE.format(
                    number=(
                        self.work.application.applicant.informations.filter(
                            date_issue__lte=self.work.application_decision_date
                        ).first(
                        ).agreements.first(
                        ).number),
                    date=date_format(
                        self.work.application.applicant.informations.filter(
                            date_issue__lte=self.work.application_decision_date
                        ).first(
                        ).agreements.first(
                        ).date_issue
                    )
                ),
            'head_of_product_certification':
                self.work.decision_head.name,
            'conclusion_application_analyze_expert':
                self.work.conclusion_expert.name
        }

    def product_evaluation_work_plan(self) -> dict:
        return {
            'head_of_product_certification':
                self.work.decision_head.name,
            'product_evaluation_work_plan_day':
                DAY_FORMAT.format(
                    date=self.work.product_evaluation_work_plan_date.day
                ),
            'product_evaluation_work_plan_month':
                MONTHS[self.work.product_evaluation_work_plan_date.month - 1],
            'product_evaluation_work_plan_year':
                f'{self.work.product_evaluation_work_plan_date.year}г.',
            'applicant_name':
                self.work.application.applicant.name,
            'prod_name':
                self.work.application.prod_name,
            'certification_decision_num_and_dt':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(self.work.release_decision_date)
                ),
            'evaluation_expert':
                self.work.evaluation_expert.name,
            'evaluation_planned_date':
                f'До {date_format(self.work.evaluation_planned_date)}',
            'evaluation_analyze_expert':
                self.work.evaluation_analyze_expert.name,
            'evaluation_analyze_planned_date':
                f'До {date_format(self.work.evaluation_analyze_planned_date)}',
            'product_evaluation_work_plan_date':
                date_format(self.work.product_evaluation_work_plan_date),
            'conclusion_application_analyze_expert':
                self.work.conclusion_expert.name
        }

    def preliminary_analysis_production_protocol(self) -> dict:
        qms_certificate_evidentiary = []
        if self.work.preliminary_analysis_production_protocol_date:
            preliminary_analysis_production_protocol_date = (
                self.work.preliminary_analysis_production_protocol_date
            )
        else:
            preliminary_analysis_production_protocol_date = "НЕ УКАЗАНА"
        for value in doc_splitter(self.work.application.docs_with_application):
            if is_qms(value):
                qms_certificate_evidentiary.append(value)

        return {
            'application_num':
                self.work.number,
            'manufacturer_name_with_location':
                MANUFACTURER_NAME_AND_LOCATION.format(
                    name=self.work.application.manufacturer.name,
                    location=self.work.application.manufacturer.location
                ),
            'manufacturer_work_location':
                "Адрес места осуществления деятельности "
                "по изготовлению продукции: "
                + self.work.application.manufacturer.work_location,
            'docs_with_application':
                self.work.application.docs_with_application.replace('\r', ''),
            'state_analysis_production_objects':
                "\n".join(qms_certificate_evidentiary),
            'conclusion_application_analyze_expert':
                self.work.conclusion_expert.name,
            'preliminary_analysis_production_protocol_date':
                preliminary_analysis_production_protocol_date
        }

    def act_analysis_production(self) -> dict:
        act_day = act_month = act_year = ""
        if self.work.act_analysis_production_date:
            act_day = DAY_FORMAT.format(
                date=self.work.act_analysis_production_date.day
            )
            act_month = MONTHS[
                self.work.act_analysis_production_date.month - 1
            ]
            act_year = f'{self.work.act_analysis_production_date.year}г.'
        qms_certificate_evidentiary = []
        for value in doc_splitter(self.work.application.docs_with_application):
            if is_qms(value):
                qms_certificate_evidentiary.append(value)

        duration_till_date = date_format(
            self.work.analysis_production_duration_till_date
        )

        return {
            'application_num':
                self.work.number,
            'act_analysis_production_day':
                act_day,
            'act_analysis_production_month':
                act_month,
            'act_analysis_production_year':
                act_year,
            'applicant_name':
                self.work.application.applicant.name,
            'prod_name':
                self.work.application.prod_name,
            'manufacturer_name_with_location_and_work_location': (
                f'Изготовитель: {self.work.application.manufacturer.name}'
                f'{self.get_manufacturer_location()}'
                f'{self.get_manufacturing_companies()}'),
            'analysis_production_duration_till_date':
                f'По {duration_till_date}',
            'application_dt':
                date_format(self.work.date),
            'analysis_production_comission_head':
                self.work.analysis_production_head.name,
            'reglament':
                self.work.application.reglament.name,
            'checked_object_status':
                "\n".join(qms_certificate_evidentiary)
                + "\n В соответствии с п.33 ТР ТС 018/2011 проверка "
                  "условий производства (выезд) не проводится.",
            'significant_decoded_name':
                self.work.application.signatory.short_name,
        }

    def expert_opinion(self):
        return {
            'application_num':
                self.work.number,
            'expert_conclusion_date':
                date_format(self.work.expert_opinion_date),
            'applicant_name':
                self.work.application.applicant.name,
            'applicant_location':
                self.work.application.applicant.informations.filter(
                    date_issue__lte=self.work.expert_opinion_date
                ).first().applicant_location,
            'applicant_work_location':
                self.work.application.applicant.informations.filter(
                    date_issue__lte=self.work.expert_opinion_date
                ).first(
                ).applicant_work_location,
            'phone_num':
                self.work.application.applicant.informations.filter(
                    date_issue__lte=self.work.expert_opinion_date
                ).first(
                ).phone_num,
            'e_mail':
                self.work.application.applicant.informations.filter(
                    date_issue__lte=self.work.expert_opinion_date
                ).first().e_mail,
            'prod_name':
                self.work.application.prod_name,
            'tn_ved_key':
                self.get_tn_ved_keys(),
            'certification_object':
                self.work.application.certification_object.name,
            'manufacturer_name':
                self.work.application.manufacturer.name,
            'manufacturer_location':
                self.work.application.manufacturer.location,
            'manufacturer_work_location':
                self.work.application.manufacturer.work_location,
            'manufacturing_companies':
                self.get_manufacturing_companies().replace(
                    MANUFACTURING_COMPANIES, ''),
            'standarts':
                self.work.application.standard.name,
            'reglament':
                self.work.application.reglament.name,
            'certification_schem':
                self.work.application.schem.name,
            'conclusion_application_analyze_expert':
                self.work.application_analyze_expert.name,
            'application_num_with_dt':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(self.work.date)
                ),
            'certification_decision_num_with_dt':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(self.work.expert_opinion_date)
                ),
            'docs_with_application_without_report':
                "".join(
                    self.get_docs_with_application_without_report()
                ).replace(
                    '\r', ''
                ),
            'report_evidentiary_and_analyze_act':
                self.get_report_evidentiary_and_analise_act(True, True),
            'decision_description':
                f'Соблюдение требований {self.work.application.reglament} '
                f'обеспечивается в результате применения на добровольной '
                f'основе '
                f'{self.work.application.standard.voluntary_docs}.'

        }

    def conclusion_of_conformity_assessment(self):
        return {
            'conclusion_of_conformity_assessment_num_with_date':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(
                        self.work.conclusion_of_conformity_assessment_date
                    )
                ),
            'certification_decision_num_and_dt':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(
                        self.work.application_decision_date
                    )
                ),
            'applicant_name':
                self.work.application.applicant.name,
            'prod_name_and_certification_object':
                f'{self.work.application.prod_name}. '
                f'{self.work.application.certification_object.name}',
            'manufacturer_name':
                f'{self.work.application.manufacturer.name}. '
                f'{self.work.application.manufacturer.country}',
            'number_of_requirenment':
                f'{self.work.application.reglament.name}\n'
                f'{self.work.application.standard.name}',
            'report_evidentiary_and_analyze_act':
                self.get_report_evidentiary_and_analise_act(
                    simple=False,
                    backspace=True
                ),
            'docs_with_application_without_report':
                "".join(
                    self.get_docs_with_application_without_report()
                ).replace(
                    '\r', ''
                ),
            'conclusion_of_conformity_assessment_expert':
                self.work.conclusion_expert.name
        }

    def release_decision(self):
        return {
            'application_num':
                self.work.number,
            'release_decision_day':
                f'«{self.work.release_decision_date.day}»',
            'release_decision_month':
                MONTHS[self.work.release_decision_date.month - 1],
            'release_decision_year':
                f'{self.work.release_decision_date.year}г.',
            'num_and_date_conclusion_of_conformity_assessment':
                NUMBER_BY_DATE.format(
                    number=self.work.number,
                    date=date_format(
                        self.work.conclusion_of_conformity_assessment_date
                    )
                ),
            'prod_name_and_certification_object':
                f'{self.work.application.prod_name}. '
                f'{self.work.application.certification_object.name}',
            'report_evidentiary_and_analyze_act':
                self.get_report_evidentiary_and_analise_act(False, True),
            'reglament':
                self.work.application.reglament.name,
            'certificate_valid_untill_date':
                date_format(self.work.certificate_expiry_date),
            'head_of_certification_body_in_certificate':
                self.work.certificate_head.full_name
        }

    def certificate_issue(self):
        applicant_data = {
            'location': self.work.application.applicant.informations.filter(
                date_issue__lte=self.work.expert_opinion_date
            ).first().applicant_location,
            'work_location':
                self.work.application.applicant.informations.filter(
                    date_issue__lte=self.work.expert_opinion_date
            ).first().applicant_work_location,
            'name': self.work.application.applicant.name,
            'ogrn': self.work.application.applicant.informations.filter(
                date_issue__lte=self.work.expert_opinion_date
            ).first().ogrn,
            'phone': self.work.application.applicant.informations.filter(
                date_issue__lte=self.work.certificate_issue_date
            ).first(
            ).phone_num,
            'e_mail': self.work.application.applicant.informations.filter(
                date_issue__lte=self.work.expert_opinion_date
            ).first().e_mail,
        }

        applicant = APPLICANT_IN_CERTIFICATE_WL_IS_L.format(
            **applicant_data
        )
        if applicant_data.get('location') != applicant_data.get(
                'work_location'
        ):
            applicant = APPLICANT_IN_CERTIFICATE_WL_IS_NOT_L.format(
                **applicant_data
            )
        return {
            'certificate_num': f'-021/S.A-{self.work.certificate_number}',
            'applicant_name_with_addresses':
                applicant,
            'manufacturer_name_with_addresses':
                (
                    f'{self.work.application.manufacturer.name}'
                    f'{self.get_manufacturer_location()}'
                    f'{self.get_manufacturing_companies()}'
                ),
            'prod_name_and_certification_object':
                f'{self.work.application.prod_name}. '
                f'{self.work.application.certification_object.name}',
            'tn_ved_key':
                self.get_tn_ved_keys(),
            'report_evidentiary_and_analyze_act_with_schem':
                self.get_report_evidentiary_and_analise_act(False, False)
                + '. Схема сертификации - '
                + self.work.application.schem.name
                + '.',
            'additional_information':
                'Соблюдение требований '
                + self.work.application.standard.name
                + ' обеспечивается в результате применения на '
                  'добровольной основе '
                + self.work.application.standard.name
                + '. Условия и сроки хранения продукции, срок службы ('
                  'ресурс) '
                + 'устанавливаются согласно документации изготовителя.',
            'cerificate_issue_date':
                date_format(self.work.certificate_issue_date),
            'certificate_valid_untill_date':
                date_format(self.work.certificate_expiry_date),
            'head_of_certification_body_in_certificate':
                self.work.certificate_head.full_name,
            "certificate_expert":
                self.work.certificate_expert.full_name
        }
