# -*- coding: UTF-8 -*-

TEMP_FILE_NAME = 'media/{name}.docx'
FORMAT = "%d.%m.%Y"
DAY_FORMAT = '« {date} »'
NUMBER_BY_DATE = '{number} от {date}'
MANUFACTURER_NAME_AND_LOCATION = '{name}\nМесто нахождения: {location}'
MONTHS = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря',
]
CONCLUSION_APPLICATION_ANALYZE_RUS = 'Заключение анализа заявки'
CONCLUSION_APPLICATION_ANALYZE = 'conclusion_application_analyze'
CERTIFICATION_DECISION_RUS = 'Решение сертификации продукции'
CERTIFICATION_DECISION = 'application_decision'
PRODUCT_EVALUATION_WORK_PLAN_RUS = 'План работ по оценке продукции'
PRODUCT_EVALUATION_WORK_PLAN = 'product_evaluation_work_plan'
PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL_RUS = (
    'Протокол предварительного анализа производства'
)
PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL = (
    'preliminary_analysis_production_protocol'
)
ACT_ANALYSIS_PRODUCTION_RUS = 'Акт анализа состояния производства'
ACT_ANALYSIS_PRODUCTION = 'act_analysis_production'
EXPERT_CONCLUSION_RUS = 'Заключение эксперта'
EXPERT_CONCLUSION = 'expert_opinion'

CHANGES = {
    CONCLUSION_APPLICATION_ANALYZE: CONCLUSION_APPLICATION_ANALYZE_RUS,
    CERTIFICATION_DECISION: CERTIFICATION_DECISION_RUS,
    PRODUCT_EVALUATION_WORK_PLAN: PRODUCT_EVALUATION_WORK_PLAN_RUS,
    PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL:
        PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL_RUS,
    ACT_ANALYSIS_PRODUCTION: ACT_ANALYSIS_PRODUCTION_RUS,
    EXPERT_CONCLUSION: EXPERT_CONCLUSION_RUS
}
PATTERNS = tuple((key, value) for key, value in CHANGES.items())
MANUFACTURER_LOCATION_IF_EXACT_WORK_LOCATION = (
    '. Место нахождения и адрес места осуществления деятельности по '
    'изготовлению продукции: {location}.'
)
MANUFACTURER_LOCATION_AND_WORK_LOCATION = (
    '. Место нахождения: {location}. Адрес места осуществления деятельности'
    ' по изготовлению продукции: {work_location}.'
)
MANUFACTURING_COMPANIES_LOCATION = '. Место нахождения: {location}'
MANUFACTURING_COMPANIES_WORK_LOCATION = (
    '. Адрес места осуществления деятельности: {work_location}'
)
PROTOCOL_FORM_START = 'Протокола испытаний №'
PROTOCOL_FORM_START_PLURAL = 'Протоколов испытаний №№'
PROTOCOL_DATE_NUMBER_FORM = '{number} от {date}г.'
PROTOCOL_FORM_FINAL = (
    'выданного {body_name}, '
    'регистрационный номер аттестата аккредитации {body_certificate}. '
)
PROTOCOL_FORM_FINAL_PLURAL = (
    'выданных {body_name}, '
    'регистрационный номер аттестата аккредитации {body_certificate}. '
)
PROTOCOL_ORDER_FIELD_NAME = 'body_certificate'

ANALYSIS_ACT_FORM = (
    "\nакта анализа состояния производства № {number} от {date}."
)
MANUFACTURING_COMPANIES = ' Производственные площадки: '
