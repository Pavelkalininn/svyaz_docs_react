# -*- coding: UTF-8 -*-
from datetime import (
    date,
    datetime,
    timedelta,
)
from typing import (
    Optional,
    Type,
)
from wsgiref.util import (
    FileWrapper,
)

from api.const import (
    ANALYSIS_ACT_MODIFIED,
    ANALYSIS_ACT_SIMPLE,
    APPLICANT_IN_CERTIFICATE_WL_IS_L,
    APPLICANT_IN_CERTIFICATE_WL_IS_NOT_L,
    APPLICANT_LOCATION_IN_APPLICATION_DIFFERENT,
    APPLICANT_LOCATION_IN_APPLICATION_EXACT,
    APPLICATION,
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
    PROTOCOL_START_MODIFIED,
    PROTOCOL_START_MODIFIED_PLURAL,
    PROTOCOL_START_SIMPLE,
    PROTOCOL_START_SIMPLE_PLURAL,
    TEMP_FILE_NAME,
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
    Application,
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


def date_format(current_date: Optional[Type[datetime.date]]) -> str:
    if current_date:
        return current_date.strftime(FORMAT)
    return ''


def doc_splitter(text: str) -> list:
    return text.replace('\r', '').split('\n')


def is_qms(text: str):
    return 'СМК' in text or '9001' in text or 'анализа состояния' in text


class FillInDocument:

    def __init__(
            self,
            work_or_application: Type[Work or Application],
            template: str
    ):

        if isinstance(work_or_application, Work):
            self.work: Work = work_or_application
            self.application = self.work.application
        else:
            self.application: Application = work_or_application
        self.template: str = template
        self.template_rus: str = CHANGES.get(self.template)

    def document_creator(self):
        work_name = self.work.name if hasattr(self, 'work') else (
            self.application.prod_name
        )[:20]
        temp_filename = self.__form_fill(work_name)
        filename = escape_uri_path(f'{self.template_rus} {work_name}')
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

    def __get_changes(self):
        return getattr(self, f'_{self.template}')()

    def __get_document_date(self):
        if self.template != APPLICATION:
            return getattr(
                self.work,
                f'{self.template}_date'
            ) or datetime.today().date()
        return datetime.today()

    def __get_docs_with_application_without_report(self):
        docs_with_application_without_report: list = []
        for value in self.application.docs_with_application:
            if "протокол" not in value and "Протокол" not in value:
                docs_with_application_without_report.append(value)
        return docs_with_application_without_report

    def __get_manufacturing_companies(self):
        manufacturing_companies = []
        if self.application.manufacturing_companies.exists():
            manufacturing_companies.append(MANUFACTURING_COMPANIES)
            for company in self.application.manufacturing_companies.all():
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

    def __get_tn_ved_keys(self):
        return ', '.join(
            str(obj.name)
            for obj in self.application.tn_ved_keys.all()
        )

    def __get_manufacturer_location(self):
        manufacturer_data = {
            'location': self.application.manufacturer.location,
            'work_location': self.application.manufacturer.work_location
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

    def __get_report_evidentiary_and_analise_act(
            self,
            simple=True,
            backspace=True
    ):
        report_evidentiary = self.__get_certificate_protocols_with_description(
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

    @staticmethod
    def __get_protocols_start(
            counter: dict,
            simple: bool,
            protocol: Protocol
    ) -> str:
        if counter.get(protocol.body_certificate) > 1:
            if simple:
                return PROTOCOL_START_SIMPLE_PLURAL
            return PROTOCOL_START_MODIFIED_PLURAL
        if simple:
            return PROTOCOL_START_SIMPLE
        return PROTOCOL_START_MODIFIED

    @staticmethod
    def __get_protocol_end(
            counter: dict,
            simple: bool,
            protocol: Protocol
    ) -> str:
        body = {
            'body_name': protocol.body_name,
            'body_certificate': protocol.body_certificate
        }
        if counter.get(protocol.body_certificate) > 1:
            if simple:
                return PROTOCOL_FINAL_SIMPLE_PLURAL.format(**body)
            return PROTOCOL_FINAL_MODIFIED_PLURAL.format(**body)
        if simple:
            return PROTOCOL_FINAL_SIMPLE.format(**body)
        return PROTOCOL_FINAL_MODIFIED.format(**body)

    def __get_certificate_protocols_with_description(
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
                or Q(applications=self.application)
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
                protocols.append(
                    first_char
                    + self.__get_protocols_start(counter, simple, protocol)
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
                protocols.append(
                    self.__get_protocol_end(counter, simple, protocol)
                    + line_break
                )
                body_protocol_count = 0
        return ' '.join(protocols)

    def __form_fill(self, work_name) -> Document:
        pattern = Pattern.objects.filter(
            date_issue__lte=self.__get_document_date(),
            name=self.template
        ).first()
        if pattern:
            doc = Document(pattern.file)
            obj_checker(doc, self.__get_changes())
            filename = escape_uri_path(
                TEMP_FILE_NAME.format(name=work_name)
            )
            doc.save(filename)
            return filename
        return None

    def _conclusion_application_analyze(self) -> dict:
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
                self.application.applicant.name,
            'prod_name':
                self.application.prod_name,
            'manufacturer_name':
                self.application.manufacturer.name,
            'tn_ved_key':
                self.__get_tn_ved_keys(),
            'docs_with_application':
                self.application.docs_with_application.replace('\r', ''),
            'number_of_requirenment':
                f'{self.application.standard.name}'
                f'\n{self.application.reglament.name}',
            'conclusion_application_analyze_expert':
                self.work.application_analyze_expert.name
        }

    def _application_decision(self) -> dict:
        recognition_evidentiary_materials = []
        qms_certificate_evidentiary = []
        for value in doc_splitter(self.application.docs_with_application):
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
        agreement = self.application.applicant.informations.filter(
                            date_issue__lte=self.work.application_decision_date
                        ).first(
                        ).agreements.first(
                        )
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
                self.application.applicant.name,
            'prod_name':
                self.application.prod_name,
            'manufacturer_name':
                self.application.manufacturer.name,
            'reglament':
                self.application.reglament.name,
            'certification_schem':
                self.application.schem.name,
            'recognition_as_evidentiary_materials':
                recognition_evidentiary_materials,
            'production_status_analysis':
                'В соответствии с п.33 ТР ТС 018/2011 провести на основании'
                ' анализа:\n'
                + '\n'.join(qms_certificate_evidentiary),
            'agreement_num_and_dt':
                NUMBER_BY_DATE.format(
                    number=agreement.number,
                    date=date_format(agreement.date_issue)
                ),
            'head_of_product_certification':
                self.work.decision_head.name,
            'conclusion_application_analyze_expert':
                self.work.conclusion_expert.name
        }

    def _product_evaluation_work_plan(self) -> dict:
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
                self.application.applicant.name,
            'prod_name':
                self.application.prod_name,
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

    def _preliminary_analysis_production_protocol(self) -> dict:
        qms_certificate_evidentiary = []
        if self.work.preliminary_analysis_production_protocol_date:
            preliminary_analysis_production_protocol_date = (
                self.work.preliminary_analysis_production_protocol_date
            )
        else:
            preliminary_analysis_production_protocol_date = "НЕ УКАЗАНА"
        for value in doc_splitter(self.application.docs_with_application):
            if is_qms(value):
                qms_certificate_evidentiary.append(value)

        return {
            'application_num':
                self.work.number,
            'manufacturer_name_with_location':
                MANUFACTURER_NAME_AND_LOCATION.format(
                    name=self.application.manufacturer.name,
                    location=self.application.manufacturer.location
                ),
            'manufacturer_work_location':
                "Адрес места осуществления деятельности "
                "по изготовлению продукции: "
                + self.application.manufacturer.work_location,
            'docs_with_application':
                self.application.docs_with_application.replace('\r', ''),
            'state_analysis_production_objects':
                "\n".join(qms_certificate_evidentiary),
            'conclusion_application_analyze_expert':
                self.work.conclusion_expert.name,
            'preliminary_analysis_production_protocol_date':
                preliminary_analysis_production_protocol_date
        }

    def _act_analysis_production(self) -> dict:
        qms_certificate_evidentiary = []
        for value in doc_splitter(self.application.docs_with_application):
            if is_qms(value):
                qms_certificate_evidentiary.append(value)

        duration_till_date = date_format(
            self.work.analysis_production_duration_till_date
        )

        return {
            'application_num':
                self.work.number,
            'act_analysis_production_day':
                DAY_FORMAT.format(
                    date=self.work.act_analysis_production_date.day
                ),
            'act_analysis_production_month':
                MONTHS[
                    self.work.act_analysis_production_date.month - 1
                ],
            'act_analysis_production_year':
                f'{self.work.act_analysis_production_date.year}г.',
            'applicant_name':
                self.application.applicant.name,
            'prod_name':
                self.application.prod_name,
            'manufacturer_name_with_location_and_work_location': (
                f'Изготовитель: {self.application.manufacturer.name}'
                f'{self.__get_manufacturer_location()}'
                f'{self.__get_manufacturing_companies()}'),
            'analysis_production_duration_till_date':
                f'По {duration_till_date}',
            'application_dt':
                date_format(self.work.date),
            'analysis_production_comission_head':
                self.work.analysis_production_head.name,
            'reglament':
                self.application.reglament.name,
            'checked_object_status':
                "\n".join(qms_certificate_evidentiary)
                + "\n В соответствии с п.33 ТР ТС 018/2011 проверка "
                  "условий производства (выезд) не проводится.",
            'significant_decoded_name':
                self.application.signatory.short_name,
        }

    def _expert_opinion(self) -> dict:
        applicant_information = self.application.applicant.informations.filter(
                    date_issue__lte=self.work.expert_opinion_date
                ).first()
        return {
            'application_num':
                self.work.number,
            'expert_conclusion_date':
                date_format(self.work.expert_opinion_date),
            'applicant_name':
                self.application.applicant.name,
            'applicant_location':
                applicant_information.applicant_location,
            'applicant_work_location':
                applicant_information.applicant_work_location,
            'phone_num':
                applicant_information.phone_num,
            'e_mail':
                applicant_information.e_mail,
            'prod_name':
                self.application.prod_name,
            'tn_ved_key':
                self.__get_tn_ved_keys(),
            'certification_object':
                self.application.certification_object.name,
            'manufacturer_name':
                self.application.manufacturer.name,
            'manufacturer_location':
                self.application.manufacturer.location,
            'manufacturer_work_location':
                self.application.manufacturer.work_location,
            'manufacturing_companies':
                self.__get_manufacturing_companies().replace(
                    MANUFACTURING_COMPANIES, ''),
            'standarts':
                self.application.standard.name,
            'reglament':
                self.application.reglament.name,
            'certification_schem':
                self.application.schem.name,
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
                    self.__get_docs_with_application_without_report()
                ).replace(
                    '\r', ''
                ),
            'report_evidentiary_and_analyze_act':
                self.__get_report_evidentiary_and_analise_act(True, True),
            'decision_description':
                f'Соблюдение требований {self.application.reglament} '
                f'обеспечивается в результате применения на добровольной '
                f'основе '
                f'{self.application.standard.voluntary_docs}.'

        }

    def _conclusion_of_conformity_assessment(self) -> dict:
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
                self.application.applicant.name,
            'prod_name_and_certification_object':
                f'{self.application.prod_name}. '
                f'{self.application.certification_object.name}',
            'manufacturer_name':
                f'{self.application.manufacturer.name}. '
                f'{self.application.manufacturer.country}',
            'number_of_requirenment':
                f'{self.application.reglament.name}\n'
                f'{self.application.standard.name}',
            'report_evidentiary_and_analyze_act':
                self.__get_report_evidentiary_and_analise_act(
                    simple=False,
                    backspace=True
                ),
            'docs_with_application_without_report':
                "".join(
                    self.__get_docs_with_application_without_report()
                ).replace(
                    '\r', ''
                ),
            'conclusion_of_conformity_assessment_expert':
                self.work.conclusion_expert.name
        }

    def _release_decision(self) -> dict:
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
                f'{self.application.prod_name}. '
                f'{self.application.certification_object.name}',
            'report_evidentiary_and_analyze_act':
                self.__get_report_evidentiary_and_analise_act(False, True),
            'reglament':
                self.application.reglament.name,
            'certificate_valid_untill_date':
                date_format(self.work.certificate_expiry_date),
            'head_of_certification_body_in_certificate':
                self.work.certificate_head.full_name
        }

    def _certificate_issue(self) -> dict:
        certificate_issue_date = (
            self.work.certificate_issue_date
            or datetime.today().date()
        )
        applicant_information = self.application.applicant.informations.filter(
                date_issue__lte=certificate_issue_date
            ).first()
        applicant_data = {
            'location': applicant_information.applicant_location,
            'work_location':
                applicant_information.applicant_work_location,
            'name': self.application.applicant.name,
            'ogrn': applicant_information.ogrn,
            'phone': applicant_information.phone_num,
            'e_mail': applicant_information.e_mail,
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
        current_year = datetime.today().year
        certificate_number = (
            self.work.certificate_number or f'0XXX-{current_year}'
        )
        data = {
            'certificate_num': f'-021/S.A-{certificate_number}',
            'applicant_name_with_addresses':
                applicant,
            'manufacturer_name_with_addresses':
                (
                    f'{self.application.manufacturer.name}'
                    f'{self.__get_manufacturer_location()}'
                    f'{self.__get_manufacturing_companies()}'
                ),
            'prod_name_and_certification_object':
                f'{self.application.prod_name}. '
                f'{self.application.certification_object.name}',
            'tn_ved_key':
                self.__get_tn_ved_keys(),
            'report_evidentiary_and_analyze_act_with_schem':
                self.__get_report_evidentiary_and_analise_act(False, False)
                + '. Схема сертификации - '
                + self.application.schem.name
                + '.',
            'additional_information':
                'Соблюдение требований '
                + self.application.standard.name
                + ' обеспечивается в результате применения на '
                  'добровольной основе '
                + self.application.standard.voluntary_docs
                + '. Условия и сроки хранения продукции, срок службы ('
                  'ресурс) '
                + 'устанавливаются согласно документации изготовителя.',
            'cerificate_issue_date':
                date_format(certificate_issue_date),
            'certificate_valid_untill_date':
                (
                    date_format(self.work.certificate_expiry_date)
                    or date(
                        datetime.today().year + 4,
                        datetime.today().month,
                        datetime.today().day
                    ) - timedelta(1)
                ),
            'head_of_certification_body_in_certificate':
                self.work.certificate_head.full_name,
            "certificate_expert":
                self.work.certificate_expert.full_name
        }
        return data

    def _application_create(self) -> dict:
        applicant_data = {
            'location':
                self.application.applicant.informations.first(
                ).applicant_location,
            'work_location':
                self.application.applicant.informations.first(
                ).applicant_work_location,
        }
        applicant_location = APPLICANT_LOCATION_IN_APPLICATION_EXACT.format(
            **applicant_data
        )
        if applicant_data.get('location') != applicant_data.get(
                'work_location'
        ):
            applicant_location = (
                APPLICANT_LOCATION_IN_APPLICATION_DIFFERENT.format(
                    **applicant_data
                )
            )
        phone = self.application.applicant.informations.first(
        ).phone_num
        e_mail = self.application.applicant.informations.first(
        ).e_mail
        manufacturer_data = {
            'location':
                self.application.manufacturer.location,
            'work_location':
                self.application.manufacturer.work_location,
        }
        manufacturer_location = (
            MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION.format(
                **manufacturer_data
            )
        )
        if manufacturer_data.get('location') != manufacturer_data.get(
                'work_location'
        ):
            manufacturer_location = (
                MANUFACTURER_LOCATION_AND_WORK_LOCATION.format(
                    **manufacturer_data
                )
            )
        return {
            'applicant_name':
                self.application.applicant.name,
            'applicant_location':
                applicant_location,
            'contacts':
                f'Номер телефона {phone}'
                f', адрес электронной почты {e_mail}',
            'applicant_representative':
                self.application.signatory.short_name,
            'prod_name':
                f'{self.application.prod_name}, '
                f'{self.application.certification_object.name}'
                ', Код ТН ВЭД ЕАЭС ' + self.__get_tn_ved_keys(),
            'manufacturer':
                self.application.manufacturer.name
                + manufacturer_location
                + '\n' + self.__get_manufacturing_companies(),
            'standarts':
                self.application.standard.name,
            'reglament':
                self.application.reglament.name,
            'schema':
                self.application.schem.name,
            'additional_information':
                self.application.additional_information,
            'docs_with_application':
                self.application.docs_with_application.replace('\r', ''),
            'significant_decoded_name':
                self.application.signatory.short_name,
        }
