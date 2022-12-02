# -*- coding: UTF-8 -*-
from datetime import (
    datetime,
)

from api.const import (
    ACT_ANALYSIS_PRODUCTION,
    CERTIFICATION_DECISION,
    CONCLUSION_APPLICATION_ANALYZE,
    DAY_FORMAT,
    FORMAT,
    MANUFACTURER_LOCATION_AND_WORK_LOCATION,
    MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION,
    MANUFACTURER_NAME_AND_LOCATION,
    MANUFACTURING_COMPANIES_LOCATION,
    MANUFACTURING_COMPANIES_WORK_LOCATION,
    MONTHS,
    NUMBER_BY_DATE,
    PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL,
    PRODUCT_EVALUATION_WORK_PLAN,
)
from documents.models import (
    Work,
)


def date_format(date: datetime.date) -> str:
    return date.strftime(FORMAT)


def doc_splitter(text: str) -> list:
    return text.replace('\r', '').split('\n')


def is_qms(text: str):
    return 'СМК' in text or '9001' in text or 'анализа состояния' in text


def conclusion_application_analyze(work: Work) -> dict:
    return {
        'conclusion_application_analyze_num_with_dt':
            NUMBER_BY_DATE.format(
                number=work.number,
                date=date_format(work.conclusion_application_analyze_date)
            ),
        'application_num_with_dt':
            NUMBER_BY_DATE.format(
                number=work.number,
                date=date_format(work.date)
            ),
        'applicant_name':
            work.application.applicant.name,
        'prod_name':
            work.application.prod_name,
        'manufacturer_name':
            work.application.manufacturer.name,
        'tn_ved_key':
            ', '.join(
                str(obj.name) for obj in work.application.tn_ved_keys.all()
            ),
        'docs_with_application':
            work.application.docs_with_application.replace('\r', ''),
        'number_of_requirenment':
            f'{work.application.standard.name}'
            f'\n{work.application.reglament.name}',
        'conclusion_application_analyze_expert':
            work.application_analyze_expert.name
    }


def certification_decision(work: Work) -> dict:
    recognition_evidentiary_materials = []
    qms_certificate_evidentiary = []
    for value in doc_splitter(work.application.docs_with_application):
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
            work.number,
        'certification_decision_day':
            DAY_FORMAT.format(
                date=work.application_decision_date.day
            ),
        'certification_decision_month':
            MONTHS.get(work.application_decision_date.month),
        'certification_decision_year':
            f'{work.application_decision_date.year}г.',
        'application_dt':
            date_format(work.date),
        'applicant_name':
            work.application.applicant.name,
        'prod_name':
            work.application.prod_name,
        'manufacturer_name':
            work.application.manufacturer.name,
        'reglament':
            work.application.reglament.name,
        'certification_schem':
            work.application.schem.name,
        'recognition_as_evidentiary_materials':
            recognition_evidentiary_materials,
        'production_status_analysis':
            'В соответствии с п.33 ТР ТС 018/2011 провести на основании'
            ' анализа:\n'
            + '\n'.join(qms_certificate_evidentiary),
        'agreement_num_and_dt':
            NUMBER_BY_DATE.format(
                number=(
                    work.application.applicant.informations.first(
                    ).agreements.first(
                    ).number),
                date=date_format(
                    work.application.applicant.informations.first(
                    ).agreements.first(
                    ).date_issue
                )
            ),
        'head_of_product_certification':
            work.decision_head.name,
        'conclusion_application_analyze_expert':
            work.conclusion_expert.name
    }


def product_evaluation_work_plan(work: Work) -> dict:
    return {
        'head_of_product_certification':
            work.decision_head.name,
        'product_evaluation_work_plan_day':
            DAY_FORMAT.format(
                date=work.product_evaluation_work_plan_date.day
            ),
        'product_evaluation_work_plan_month':
            MONTHS.get(work.product_evaluation_work_plan_date.month),
        'product_evaluation_work_plan_year':
            f'{work.product_evaluation_work_plan_date.year}г.',
        'applicant_name':
            work.application.applicant.name,
        'prod_name':
            work.application.prod_name,
        'certification_decision_num_and_dt':
            NUMBER_BY_DATE.format(
                number=work.number,
                date=date_format(work.release_decision_date)
            ),
        'evaluation_expert':
            work.evaluation_expert.name,
        'evaluation_planned_date':
            f'До {date_format(work.evaluation_planned_date)}',
        'evaluation_analyze_expert':
            work.evaluation_analyze_expert.name,
        'evaluation_analyze_planned_date':
            f'До {date_format(work.evaluation_analyze_planned_date)}',
        'product_evaluation_work_plan_date':
            date_format(work.product_evaluation_work_plan_date),
        'conclusion_application_analyze_expert':
            work.conclusion_expert.name
    }


def preliminary_analysis_production_protocol(work: Work) -> dict:
    qms_certificate_evidentiary = []
    if work.preliminary_analysis_production_protocol_date:
        preliminary_analysis_production_protocol_date = (
            work.preliminary_analysis_production_protocol_date
        )
    else:
        preliminary_analysis_production_protocol_date = "НЕ УКАЗАНА"
    for value in doc_splitter(work.application.docs_with_application):
        if is_qms(value):
            qms_certificate_evidentiary.append(value)

    return {
        'application_num':
            work.number,
        'manufacturer_name_with_location':
            MANUFACTURER_NAME_AND_LOCATION.format(
                name=work.application.manufacturer.name,
                location=work.application.manufacturer.location
            ),
        'manufacturer_work_location':
            "Адрес места осуществления деятельности "
            "по изготовлению продукции: "
            + work.application.manufacturer.work_location,
        'docs_with_application':
            work.application.docs_with_application.replace('\r', ''),
        'state_analysis_production_objects':
            "\n".join(qms_certificate_evidentiary),
        'conclusion_application_analyze_expert':
            work.conclusion_expert.name,
        'preliminary_analysis_production_protocol_date':
            preliminary_analysis_production_protocol_date
    }


def act_analysis_production(work: Work) -> dict:
    if work.act_analysis_production_date:
        act_day = DAY_FORMAT.format(
            date=work.act_analysis_production_date.day
        )
        act_month = MONTHS.get(work.act_analysis_production_date.month)
        act_year = f'{work.act_analysis_production_date.year}г.'
    else:
        act_day = act_month = act_year = ""
    qms_certificate_evidentiary = []
    for value in doc_splitter(work.application.docs_with_application):
        if is_qms(value):
            qms_certificate_evidentiary.append(value)
    if (
            work.application.manufacturer.location
            in (work.application.manufacturer.work_location, )
    ):
        manufacturer_location_and_work_location = (
            MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION.format(
                location=work.application.manufacturer.location
            )
        )
    else:
        manufacturer_location_and_work_location = (
            MANUFACTURER_LOCATION_AND_WORK_LOCATION.format(
                location=work.application.manufacturer.location,
                work_location=work.application.manufacturer.work_location
            )
        )

    manufacturing_companies = []
    if work.application.manufacturing_companies.exists():
        manufacturing_companies.append(' Производственные площадки: ')
        for company in work.application.manufacturing_companies.all():
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
    manufacturing_companies = ''.join(manufacturing_companies)

    return {
        'application_num':
            work.number,
        'act_analysis_production_day':
            act_day,
        'act_analysis_production_month':
            act_month,
        'act_analysis_production_year':
            act_year,
        'applicant_name':
            work.application.applicant.name,
        'prod_name':
            work.application.prod_name,
        'manufacturer_name_with_location_and_work_location': (
            f'Изготовитель: {work.application.manufacturer.name}'
            f'{manufacturer_location_and_work_location}'
            f'{manufacturing_companies}'),
        'analysis_production_duration_till_date':
            f'По {date_format(work.analysis_production_duration_till_date)}',
        'application_dt':
            date_format(work.date),
        'analysis_production_comission_head':
            work.analysis_production_head.name,
        'reglament':
            work.application.reglament.name,
        'checked_object_status':
            "\n".join(qms_certificate_evidentiary)
            + "\n В соответствии с п.33 ТР ТС 018/2011 проверка "
              "условий производства (выезд) не проводится.",
        'significant_decoded_name':
            work.application.signatory.short_name,
    }


CHANGES = {
    CONCLUSION_APPLICATION_ANALYZE:
        (
            conclusion_application_analyze,
            'conclusion_application_analyze_date'
        ),
    CERTIFICATION_DECISION:
        (
            certification_decision,
            'application_decision_date'
        ),
    PRODUCT_EVALUATION_WORK_PLAN:
        (
            product_evaluation_work_plan,
            'product_evaluation_work_plan_date'
        ),
    PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL:
        (
            preliminary_analysis_production_protocol,
            'preliminary_analysis_production_protocol_date'
        ),
    ACT_ANALYSIS_PRODUCTION:
        (
            act_analysis_production,
            'act_analysis_production_date'
        )
}
