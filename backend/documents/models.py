from api.const import (
    PATTERNS,
)
from django.contrib.auth.models import (
    AbstractUser,
)
from django.core.validators import (
    RegexValidator,
)
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    CharField,
    DateField,
    EmailField,
    FileField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveBigIntegerField,
    TextField,
    UniqueConstraint,
)

from backend.settings import (
    CHAR_FIELD_MAX_SIZE,
    CHAR_FIELD_MIDDLE_SIZE,
    CHAR_FIELD_PHONE_SIZE,
    CHAR_FIELD_SMALL_SIZE,
    EMAIL_REGEX,
    FULL_NAME_REGEX,
    GTIN_REGEX,
    INITIALS_REGEX,
    PHONE_REGEX,
    USER_ROLE_CHOICES,
)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    username = CharField(
        unique=True,
        max_length=150,
        verbose_name='Логин',
        validators=(RegexValidator(regex=r'^[\w.@+-]+\Z'), )
    )
    first_name = CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    email = EmailField(
        unique=True,
        max_length=254,
        verbose_name='Почта'
    )
    role = CharField(
        'Роль',
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default='user'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


class Applicant(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование заявителя'
    )
    owner = ForeignKey(
        User,
        related_name='owner_applicants',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'заявитель'
        verbose_name_plural = 'Заявители'


class Signatory(Model):
    short_name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    full_name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Полное фамилия имя отчество',
        validators=(
            RegexValidator(
                regex=FULL_NAME_REGEX
            ),
        )
    )
    position = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Должность'
    )

    applicant = ForeignKey(
        Applicant,
        related_name='signatories',
        verbose_name='заявитель',
        on_delete=CASCADE
    )
    owner = ForeignKey(
        User,
        related_name='signatories',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ['short_name']
        verbose_name = 'подписант'
        verbose_name_plural = 'Подписанты'
        constraints = [
            UniqueConstraint(
                fields=['short_name', 'position'],
                name='unique_signatory'),
        ]


class Proxy(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='номер/наименование'
    )
    date_issue = DateField(
        verbose_name='дата выдачи'
    )
    date_expiry = DateField(
        null=True,
        blank=True,
        verbose_name='дата окончания действия'
    )
    signatory = ForeignKey(
        Signatory,
        related_name='proxies',
        verbose_name='Подписант',
        on_delete=CASCADE
    )
    owner = ForeignKey(
        User,
        related_name='proxies',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_issue']
        verbose_name = 'доверенность'
        verbose_name_plural = 'Доверенности'


class ApplicantInformation(Model):
    ogrn = PositiveBigIntegerField(
        verbose_name='ОГРН',
    )
    inn = PositiveBigIntegerField(
        verbose_name='ИНН',
    )
    applicant_location = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='адрес места нахождения заявителя'
    )
    applicant_work_location = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='адрес места осуществления деятельности заявителя'
    )
    phone_num = CharField(
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер телефона, начиная с "+"',
        validators=(
            RegexValidator(
                regex=PHONE_REGEX
            ),
        )
    )
    e_mail = CharField(
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='e-mail',
        validators=(
            RegexValidator(
                regex=EMAIL_REGEX
            ),
        )
    )
    date_issue = DateField(
        verbose_name='дата начала актуальности этих документов'
    )
    date_expiry = DateField(
        null=True,
        blank=True,
        verbose_name='дата окончания актуальности этих документов'
    )
    applicant = ForeignKey(
        Applicant,
        related_name='informations',
        verbose_name='Заявитель',
        on_delete=CASCADE
    )
    owner = ForeignKey(
        User,
        related_name='applicant_informations',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.applicant_location

    class Meta:
        ordering = ['-date_issue']
        verbose_name = 'карточка организации'
        verbose_name_plural = 'Карточки организации'
        constraints = [
            UniqueConstraint(
                fields=['ogrn', 'date_issue'],
                name='unique_applicant_information'),
        ]


class Agreement(Model):
    number = CharField(
        unique=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Номер соглашения'
    )
    date_issue = DateField(
        verbose_name='Дата соглашения'
    )
    date_expiry = DateField(
        null=True,
        blank=True,
        verbose_name='Срок действия'
    )
    applicant_information = ForeignKey(
        ApplicantInformation,
        related_name='agreements',
        verbose_name='параметры заявителя',
        on_delete=CASCADE
    )
    owner = ForeignKey(
        User,
        related_name='agreements',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['-date_issue']
        verbose_name = 'соглашение'
        verbose_name_plural = 'Соглашения'


class Standard(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование стандарта'
    )
    voluntary_docs = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Документы применяемые на добровольной основе'
    )
    requirement_name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование требования'
    )
    short_requirement_name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Короткое наименование требования (только номер)'
    )
    requirement_modify_name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование пунктов и таблиц из ТР ТС'
    )
    methods = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Методы испытаний'
    )
    standard = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='стандарты!?'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'стандарт'
        verbose_name_plural = 'Стандарты'


class CertificationObject(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='объект сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'объект сертификации'
        verbose_name_plural = 'Объекты сертификации'


class Reglament(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='регламент'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'регламент'
        verbose_name_plural = 'Регламенты'


class Schem(Model):
    name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='схема сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'схема сертификации'
        verbose_name_plural = 'Схемы сертификации'


class TnVedKey(Model):
    name = PositiveBigIntegerField(
        unique=True,
        verbose_name='Код ТН ВЭД ЕАЭС'
    )
    description = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Описание'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'код ТН ВЭД ЕАЭС'
        verbose_name_plural = 'Коды ТН ВЭД ЕАЭС'


class Manufacturer(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование изготовителя'
    )
    location = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Адрес места нахождения изготовителя'
    )
    work_location = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Адрес места осуществления изготовителя'
    )
    country = CharField(
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='Страна изготовления'
    )
    owner = ForeignKey(
        User,
        related_name='manufacturers',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'изготовитель'
        verbose_name_plural = 'Изготовители'
        constraints = [
            UniqueConstraint(
                fields=['name', 'location', 'work_location'],
                name='unique_manufacturer'
            ),
        ]


class QMS(Model):
    number = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Номер сертификата СМК'
    )
    date_issue = DateField(
        verbose_name='Дата выдачи'
    )
    date_expiry = DateField(
        verbose_name='Дата окончания действия'
    )
    body_certificate = CharField(
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='Аттестат аккредитации органа по сертификации СМК'
    )
    body_name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование органа по сертификации СМК'
    )
    signatory = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы эксперта в сертификате СМК',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    manufacturer = ForeignKey(
        Manufacturer,
        related_name='qms',
        verbose_name='Изготовитель',
        on_delete=CASCADE
    )
    owner = ForeignKey(
        User,
        related_name='qms',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']
        verbose_name = 'сертификат СМК'
        verbose_name_plural = 'Сертификаты СМК'


class ConfirmationDecision(Model):
    number = CharField(
        unique=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Наименование решения о подтверждении СМК'
    )
    date = DateField(
        verbose_name='Дата решения о подтверждении СМК'
    )
    signatory = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы эксперта в решении о подтверждении',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    qms = ForeignKey(
        QMS,
        related_name='confirmation_decisions',
        verbose_name='Сертификат СМК',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']
        verbose_name = 'решение о подтверждении СМК'
        verbose_name_plural = 'Решения о подтверждении СМК'


class ManufacturingCompany(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование производственной площадки'
    )
    location = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Место нахождения производственной площадки'
    )
    work_location = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Место осуществления производственной площадки'
    )
    manufacturer = ForeignKey(
        Manufacturer,
        related_name='manufacturing_companies',
        verbose_name='Изготовитель',
        on_delete=CASCADE
    )
    owner = ForeignKey(
        User,
        related_name='manufacturing_companies',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'производственная площадка'
        verbose_name_plural = 'Производственные площадки'
        constraints = [
            UniqueConstraint(
                fields=['name', 'location', 'work_location'],
                name='unique_manufacturing_companies'),
        ]


class CertificationBody(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование органа'
    )
    attestation = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Аттестат аккредитации'
    )
    attestation_date = DateField(
        verbose_name='Дата выдачи аттестата'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'орган по сертификации продукции'
        verbose_name_plural = 'Органы по сертфикации продукции'


class Expert(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы эксперта',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    full_name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Полное фамилия имя отчество эксперта',
        validators=(
            RegexValidator(
                regex=FULL_NAME_REGEX
            ),
        )
    )
    body = ForeignKey(
        CertificationBody,
        related_name='experts',
        verbose_name='Орган по сертификации',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'эксперт'
        verbose_name_plural = 'Эксперты'


class Head(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы руководителя',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    full_name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Полное фамилия имя отчество руководителя',
        validators=(
            RegexValidator(
                regex=FULL_NAME_REGEX
            ),
        )
    )
    body = ForeignKey(
        CertificationBody,
        related_name='head',
        verbose_name='Орган по сертификации',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'руководитель органа'
        verbose_name_plural = 'Руководители органов'


class Protocol(Model):
    number = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Номер протокола'
    )
    date = DateField(
        verbose_name='Дата протокола'
    )
    body_certificate = CharField(
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='Аттестат аккредитации испытательной лаборатории'
    )
    body_name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name=(
            'Полное наименование лаборатории в творительном падеже (кем?)'
            ' (испытательной лабораторией ...)'
        )
    )
    signatory = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы руководителя ИЛ в протоколе',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    owner = ForeignKey(
        User,
        related_name='protocols',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return f'{self.number} от {self.date}'

    class Meta:
        ordering = ['number']
        verbose_name = 'протокол'
        verbose_name_plural = 'Протоколы'
        constraints = [
            UniqueConstraint(
                fields=['number', 'owner'],
                name='unique_applicant_protocol'),
        ]


class Application(Model):
    applicant = ForeignKey(
        Applicant,
        related_name='applications',
        verbose_name='заявитель',
        on_delete=CASCADE
    )
    certification_body = ForeignKey(
        CertificationBody,
        related_name='applications',
        verbose_name='Орган по сертификации',
        on_delete=CASCADE
    )
    signatory = ForeignKey(
        Signatory,
        related_name='applications',
        verbose_name='подписант',
        on_delete=DO_NOTHING
    )
    standard = ForeignKey(
        Standard,
        related_name='applications',
        verbose_name='стандарт',
        on_delete=CASCADE
    )
    GTIN_key = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Код GTIN',
        validators=(
            RegexValidator(
                regex=GTIN_REGEX
            ),
        )
    )
    certification_object = ForeignKey(
        CertificationObject,
        related_name='applications',
        verbose_name='объект сертификации',
        on_delete=CASCADE
    )
    reglament = ForeignKey(
        Reglament,
        related_name='applications',
        verbose_name='регламент',
        on_delete=CASCADE
    )
    schem = ForeignKey(
        Schem,
        related_name='applications',
        verbose_name='схема сертификации',
        on_delete=CASCADE
    )
    applicant_representative_who_doing_application = ForeignKey(
        Signatory,
        related_name='representative_to_applications',
        verbose_name='представитель заявителя',
        on_delete=CASCADE
    )
    prod_name = TextField(
        verbose_name='Наименование продукции'
    )
    tn_ved_keys = ManyToManyField(
        TnVedKey,
        related_name='applications',
    )
    manufacturer = ForeignKey(
        Manufacturer,
        related_name='applications',
        verbose_name='Изготовитель',
        on_delete=CASCADE
    )
    manufacturing_companies = ManyToManyField(
        ManufacturingCompany,
        related_name='applications',
        verbose_name='Производственные площадки',
    )
    protocols = ManyToManyField(
        Protocol,
        verbose_name='Протоколы испытаний приложенные к заявке'
    )
    qms = ForeignKey(
        QMS,
        related_name='applications',
        verbose_name='Сертификат СМК',
        on_delete=CASCADE
    )
    docs_with_application = TextField(
        verbose_name='Предоставленные с заявкой документы'
    )
    additional_information = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Дополнительная информация'
    )
    owner = ForeignKey(
        User,
        related_name='applications',
        verbose_name='Владелец',
        on_delete=CASCADE
    )

    def __str__(self):
        return f'{self.applicant} {self.standard} {self.prod_name}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'заявка'
        verbose_name_plural = 'Заявки'


class Work(Model):
    name = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Условное наименование работы'
    )
    application = OneToOneField(
        Application,
        unique=True,
        related_name='work',
        verbose_name='заявка',
        on_delete=CASCADE
    )
    path_to_folder = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='путь к папке с работой',
    )
    number = CharField(
        unique=True,
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Номер заявки'
    )
    date = DateField(
        verbose_name='Дата заявки'
    )
    application_analyze_expert = ForeignKey(
        Expert,
        null=True,
        blank=True,
        related_name='application_analyze_expert_works',
        verbose_name='Эксперт в заключении анализа',
        on_delete=CASCADE
    )
    evaluation_expert = ForeignKey(
        Expert,
        null=True,
        blank=True,
        related_name='evaluation_expert_works',
        verbose_name='Эксперт ответственный за оценивание',
        on_delete=CASCADE
    )
    evaluation_analyze_expert = ForeignKey(
        Expert,
        null=True,
        blank=True,
        related_name='evaluation_analyze_expert_works',
        verbose_name='Эксперт по анализу результатов оценивания',
        on_delete=CASCADE
    )
    analysis_production_head = ForeignKey(
        Expert,
        null=True,
        blank=True,
        related_name='analysis_production_head_works',
        verbose_name='Руководитель комиссии',
        on_delete=CASCADE
    )
    conclusion_expert = ForeignKey(
        Expert,
        null=True,
        blank=True,
        related_name='conclusion_expert_works',
        verbose_name='Эксперт в заключении',
        on_delete=CASCADE
    )
    certificate_expert = ForeignKey(
        Expert,
        null=True,
        blank=True,
        related_name='certificate_expert_works',
        verbose_name='Эксперт в сертификате',
        on_delete=CASCADE
    )

    decision_head = ForeignKey(
        Head,
        null=True,
        blank=True,
        related_name='decision_head_works',
        verbose_name='Руководитель ОС в решении о проведении',
        on_delete=CASCADE
    )
    certificate_head = ForeignKey(
        Head,
        null=True,
        blank=True,
        related_name='certificate_head_works',
        verbose_name='Руководитель в сертификате',
        on_delete=CASCADE
    )
    conclusion_application_analyze_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата заключения анализа заявки'
    )
    application_decision_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата решения по заявке'
    )
    evaluation_planned_date = DateField(
        null=True,
        blank=True,
        verbose_name='Запланированный срок оценивания'
    )
    evaluation_analyze_planned_date = DateField(
        null=True,
        blank=True,
        verbose_name='Запланированный срок анализа результатов оценивания'
    )
    preliminary_analysis_production_protocol_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата протокола предварительного анализа производства'
    )
    act_analysis_production_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата акта анализа состояния производства'
    )
    analysis_production_duration_till_date = DateField(
        null=True,
        blank=True,
        verbose_name='Срок проведения анализа сотсояния производства (По)'
    )
    conclusion_of_conformity_assessment_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата заключения анализа'
    )
    analysis_production_registry_notes = DateField(
        null=True,
        blank=True,
        verbose_name='Примечания по регистрации анализа состояния продукции'
    )

    product_evaluation_work_plan_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата плана работ по оценке'
    )
    expert_opinion_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата заключения эксперта'
    )
    release_decision_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата решения о выдаче'
    )
    certificate_issue_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата заключения эксперта'
    )
    certificate_expiry_date = DateField(
        null=True,
        blank=True,
        verbose_name='Дата выдачи сертификата'
    )
    certificate_number = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер сертификата'
    )
    certificate_application_1_form_number = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер формы приложения 1 к сертификату'
    )
    certificate_application_2_form_number = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер формы приложения 2 к сертификату'
    )
    application_registration_form_notes = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name=(
            'Примечания по регистрации заявки (в форму регистрации заявок)'
        )
    )
    registry_certificate_confirmation_notes = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name=(
            'Примечания о выдаче сертификата (в форму регистрации заявок)'
        )
    )
    sampling_identification_with_dt = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name=(
            'Отбор образцов, заключение идентификации,'
            ' дата (для Формы регистрации заявок)'
        )
    )
    directing_with_dt = CharField(
        null=True,
        blank=True,
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='№ направления в ИЛ, дата (для Формы регистрации заявок)'
    )
    protocols = ManyToManyField(
        Protocol,
        verbose_name='Протоколы испытаний полученные в ходе сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'работа органа'
        verbose_name_plural = 'Работы органа'


class Pattern(Model):
    name = CharField(
        'Наименование формы',
        max_length=CHAR_FIELD_MAX_SIZE,
        choices=PATTERNS,
    )
    date_issue = DateField(
        'Дата начала использования'
    )
    file = FileField(
        unique=True,
        upload_to='patterns',
    )

    def __str__(self):
        return f'{self.name} от {self.date_issue}'

    class Meta:
        ordering = ['name', '-date_issue']
        verbose_name = 'форма документа'
        verbose_name_plural = 'Формы документов'
