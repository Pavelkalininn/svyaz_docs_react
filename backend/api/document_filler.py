# -*- coding: UTF-8 -*-
from datetime import (
    datetime,
)
from wsgiref.util import FileWrapper

import docx
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from docx import Document
from rest_framework import status
from rest_framework.response import Response

from api.const import (
    DAY_FORMAT,
    FORMAT,
    MANUFACTURER_NAME_AND_LOCATION,
    MONTHS,
    NUMBER_BY_DATE, MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION,
    MANUFACTURER_LOCATION_AND_WORK_LOCATION,
    MANUFACTURING_COMPANIES_WORK_LOCATION,
    MANUFACTURING_COMPANIES_LOCATION,
    PROTOCOL_DATE_NUMBER_FORM, PROTOCOL_FORM_START_PLURAL, PROTOCOL_FORM_START,
    PROTOCOL_FORM_FINAL_PLURAL, PROTOCOL_FORM_FINAL, PROTOCOL_ORDER_FIELD_NAME,
    ANALYSIS_ACT_FORM, TEMP_FILE_NAME, CHANGES, MANUFACTURING_COMPANIES,
)
from api.utils import obj_checker

from documents.models import Work, Protocol, Pattern


def date_format(date: datetime.date) -> str:
    return date.strftime(FORMAT)


def doc_splitter(text: str) -> list:
    return text.replace('\r', '').split('\n')


def is_qms(text: str):
    return 'СМК' in text or '9001' in text or 'анализа состояния' in text


class FillInDocument:

    def __init__(self, work, template):
        self.work = work
        self.template = template
        self.template_rus = CHANGES.get(self.template)

    def get_changes(self):
        return getattr(self, self.template)()

    def get_document_date(self):
        return getattr(self.work, f'{self.template}_date')

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

    def get_certificate_protocols_with_description(self) -> str:
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
        for protocol in provided_protocols:
            if body_protocol_count == 0:
                if counter.get(protocol.body_certificate) > 1:
                    protocols.append(PROTOCOL_FORM_START_PLURAL)
                else:
                    protocols.append(PROTOCOL_FORM_START)
            body_protocol_count += 1
            if body_protocol_count != counter.get(protocol.body_certificate):
                protocols.append(
                    PROTOCOL_DATE_NUMBER_FORM.format(
                        number=protocol.number,
                        date=date_format(protocol.date)
                    ) + ','
                )
            else:
                protocols.append(
                    PROTOCOL_DATE_NUMBER_FORM.format(
                        number=protocol.number,
                        date=date_format(protocol.date)
                    )
                )
                if counter.get(protocol.body_certificate) > 1:
                    protocols.append(
                        PROTOCOL_FORM_FINAL_PLURAL.format(
                            body_name=protocol.body_name,
                            body_certificate=protocol.body_certificate
                        )
                    )
                else:
                    protocols.append(
                        PROTOCOL_FORM_FINAL.format(
                            body_name=protocol.body_name,
                            body_certificate=protocol.body_certificate
                        )
                    )
                body_protocol_count = 0
        return ' '.join(protocols)

    def document_creator(self):
        file = self.form_fill()
        filename = escape_uri_path(f'{self.template_rus} {self.work.name}')
        if file:
            with open(file, 'rb') as worddoc:
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
                MONTHS[self.work.application_decision_date.month],
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
                MONTHS[self.work.product_evaluation_work_plan_date.month],
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
        if self.work.act_analysis_production_date:
            act_day = DAY_FORMAT.format(
                date=self.work.act_analysis_production_date.day
            )
            act_month = MONTHS[self.work.act_analysis_production_date.month]
            act_year = f'{self.work.act_analysis_production_date.year}г.'
        else:
            act_day = act_month = act_year = ""
        qms_certificate_evidentiary = []
        for value in doc_splitter(self.work.application.docs_with_application):
            if is_qms(value):
                qms_certificate_evidentiary.append(value)
        if (
                self.work.application.manufacturer.location
                in (self.work.application.manufacturer.work_location,)
        ):
            manufacturer_location_and_work_location = (
                MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION.format(
                    location=self.work.application.manufacturer.location
                )
            )
        else:
            manufacturer_location_and_work_location = (
                MANUFACTURER_LOCATION_AND_WORK_LOCATION.format(
                    location=self.work.application.manufacturer.location,
                    work_location=(
                        self.work.application.manufacturer.work_location
                    )
                )
            )

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
                f'{manufacturer_location_and_work_location}'
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
        report_evidentiary = self.get_certificate_protocols_with_description(

        ) or ''
        analysis_act = ''
        if self.work.act_analysis_production_date:
            analysis_act = ANALYSIS_ACT_FORM.format(
                number=self.work.number,
                date=date_format(self.work.act_analysis_production_date)
            )

        report_evidentiary_and_analyze_act = report_evidentiary + analysis_act
        docs_with_application_without_report = (
            self.work.application.docs_with_application
        )
        for value in docs_with_application_without_report:
            if "протокол" in value or "Протокол" in value:
                docs_with_application_without_report.remove(value)
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
                "".join(docs_with_application_without_report).replace(
                    '\r', ''
                ),
            'report_evidentiary_and_analyze_act':
                report_evidentiary_and_analyze_act,
            'decision_description':
                f'Соблюдение требований {self.work.application.reglament} '
                f'обеспечивается в результате применения на добровольной '
                f'основе '
                f'{self.work.application.standard.voluntary_docs}.'

        }

# def certification_decision(work):
#     return {
#
#     }
