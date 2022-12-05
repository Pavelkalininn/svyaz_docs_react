# -*- coding: UTF-8 -*-

TEMP_FILE_NAME = 'temp.docx'
FORMAT = "%d.%m.%Y"
DAY_FORMAT = '« {date} »'
NUMBER_BY_DATE = '{number} от {date}'
MANUFACTURER_NAME_AND_LOCATION = '{name}\nМесто нахождения: {location}'
MONTHS = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}
CONCLUSION_APPLICATION_ANALYZE = 'Заключение анализа заявки'
CERTIFICATION_DECISION = 'Решение сертификации продукции'
PRODUCT_EVALUATION_WORK_PLAN = 'План работ по оценке продукции'
PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL = (
    'Протокол предварительного анализа производства'
)
ACT_ANALYSIS_PRODUCTION = 'Акт анализа состояния производства'
EXPERT_CONCLUSION = 'Заключение эксперта'

PATTERNS = (
    (CONCLUSION_APPLICATION_ANALYZE, CONCLUSION_APPLICATION_ANALYZE),
    (CERTIFICATION_DECISION, CERTIFICATION_DECISION),
    (PRODUCT_EVALUATION_WORK_PLAN, PRODUCT_EVALUATION_WORK_PLAN),
    (
        PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL,
        PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL
    ),
    (EXPERT_CONCLUSION, EXPERT_CONCLUSION)

)
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
