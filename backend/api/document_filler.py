# -*- coding: UTF-8 -*-
from datetime import (
    datetime,
)

from api.const import (
    CERTIFICATION_DECISION,
    CONCLUSION_APPLICATION_ANALYZE,
    DAY_FORMAT,
    FORMAT,
    MANUFACTURER_NAME_AND_LOCATION,
    MONTHS,
    NUMBER_BY_DATE,
    PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL,
    PRODUCT_EVALUATION_WORK_PLAN,
)


def date_format(date: datetime.date):
    return date.strftime(FORMAT)


def conclusion_application_analyze(work):
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


def certification_decision(work):
    recognition_evidentiary_materials = []
    qms_certificate_evidentiary = []
    for value in work.application.docs_with_application.replace(
            '\r', ''
    ).split('\n'):
        if 'СМК' in value or '9001' in value or 'анализа состояния' in value:
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


def product_evaluation_work_plan(work):
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


def preliminary_analysis_production_protocol(work):
    qms_certificate_evidentiary = []
    if work.preliminary_analysis_production_protocol_date:
        preliminary_analysis_production_protocol_date = (
            work.preliminary_analysis_production_protocol_date
        )
    else:
        preliminary_analysis_production_protocol_date = "НЕ УКАЗАНА"
    for value in work.application.docs_with_application.replace(
            '\r', ''
    ).split('\n'):
        if (
                'СМК' in value
                or '9001' in value
                or 'анализа состояния' in value
        ):
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
        'preliminary_analysys_production_protocol_date':
            preliminary_analysis_production_protocol_date
    }


# def certification_decision(work):
#     return {
#
#     }

# def certification_decision(work):
#     return {
#
#     }


# def certification_decision(work):
#     return {
#
#     }


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
        )
}
