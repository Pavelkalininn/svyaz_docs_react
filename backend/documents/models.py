from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    FilePathField,
    Model,
    CASCADE,
    PositiveBigIntegerField,
    DO_NOTHING, TextField, ManyToManyField, EmailField, OneToOneField,
)

from backend.settings import (
    INITIALS_REGEX,
    FULL_NAME_REGEX,
    PHONE_REGEX,
    EMAIL_REGEX,
    GTIN_REGEX,
    CHAR_FIELD_MAX_SIZE,
    CHAR_FIELD_MIDDLE_SIZE,
    CHAR_FIELD_SMALL_SIZE, CHAR_FIELD_PHONE_SIZE, USER_ROLE_CHOICES
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
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Application(Model):
    number = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Номер заявки'
    )
    date = DateField(
        verbose_name='Дата заявки'
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['-date']


class Proxy(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='номер/наименование'
    )
    date_issue = DateField(
        verbose_name='дата выдачи'
    )
    date_expiry = DateField(
        verbose_name='дата окончания действия'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_issue']


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
    proxy = ForeignKey(
        Proxy,
        related_name='signatory',
        verbose_name='доверенность',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ['short_name']


class Agreement(Model):
    number = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Номер соглашения'
    )
    date_issue = DateField(
        verbose_name='Дата соглашения'
    )
    date_expiry = DateField(
        verbose_name='Срок действия'
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['-date_issue']


class ApplicantInformation(Model):
    agreements = ForeignKey(
        Agreement,
        related_name='applicant_information',
        verbose_name='соглашения',
        on_delete=CASCADE
    )
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
        verbose_name='дата окончания актуальности этих документов'
    )

    def __str__(self):
        return self.applicant_location

    class Meta:
        ordering = ['-date_issue']


class Applicant(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Условное наименование работы'
    )
    signatories = ForeignKey(
        Signatory,
        related_name='applicant',
        verbose_name='подписанты',
        on_delete=CASCADE
    )
    informations = ForeignKey(
        ApplicantInformation,
        related_name='applicant',
        verbose_name='информация о заявителе (документы)',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Standard(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование стандарта'
    )
    voluntary_docs = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Документы применяемые на добровольной основе'
    )
    requirement_name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование требования'
    )
    short_requirement_name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Короткое наименование требования (только номер)'
    )
    requirement_modify_name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование пунктов и таблиц из ТР ТС'
    )
    methods = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Методы испытаний'
    )
    standard = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='стандарты!?'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CertificationObject(Model):
    name = CharField(
        max_length=CHAR_FIELD_SMALL_SIZE,
        verbose_name='объект сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Reglament(Model):
    name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='регламент'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Schem(Model):
    name = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='схема сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TnVedKey(Model):
    name = PositiveBigIntegerField(
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


class ConfirmationDecision(Model):
    number = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Наименование решения о подтверждении СМК'
    )
    date = DateField(
        verbose_name='Дата решения о подтверждении СМК'
    )
    signatory = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы эксперта в решении о подтверждении',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']


class ManufacturingCompanies(Model):
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class QMS(Model):
    number = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Наименование изготовителя'
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
        verbose_name='НАименование органа по сертификации СМК'
    )
    signatory = CharField(
        max_length=CHAR_FIELD_MIDDLE_SIZE,
        verbose_name='Фамилия и инициалы эксперта в сертификате СМК',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    confirmation_decision = ForeignKey(
        ConfirmationDecision,
        related_name='qms',
        verbose_name='Решение о подтверждении СМК',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']


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
    manufacturing_companies = ForeignKey(
        ManufacturingCompanies,
        related_name='manufacturer',
        verbose_name='Производственные площадки',
        on_delete=CASCADE
    )
    qms = ForeignKey(
        QMS,
        related_name='manufacturer',
        verbose_name='Сертификат СМК',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Expert(Model):
    name = CharField(
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Head(Model):
    name = CharField(
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CertificationBody(Model):
    name = CharField(
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
    experts = ForeignKey(
        Expert,
        related_name='body',
        verbose_name='Эксперты',
        on_delete=CASCADE
    )
    head = ForeignKey(
        Head,
        related_name='body',
        verbose_name='Руководители',
        on_delete=CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Project(Model):
    name = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Условное наименование работы'
    )
    certification_body = ForeignKey(
        CertificationBody,
        related_name='projects',
        verbose_name='Орган по сертификации',
        on_delete=CASCADE
    )
    application = OneToOneField(
        Application,
        related_name='projects',
        verbose_name='заявка',
        on_delete=CASCADE
    )
    path_to_folder = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='путь к папке с работой',
    )
    applicant = ForeignKey(
        Applicant,
        related_name='projects',
        verbose_name='заявитель',
        on_delete=CASCADE
    )
    signatory = ForeignKey(
        Signatory,
        related_name='projects',
        verbose_name='подписант',
        on_delete=DO_NOTHING
    )
    standard = ForeignKey(
        Standard,
        related_name='projects',
        verbose_name='стандарт',
        on_delete=CASCADE
    )
    GTIN_key = CharField(
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
        related_name='projects',
        verbose_name='объект сертификации',
        on_delete=CASCADE
    )
    reglament = ForeignKey(
        Reglament,
        related_name='projects',
        verbose_name='регламент',
        on_delete=CASCADE
    )
    schem = ForeignKey(
        Schem,
        related_name='projects',
        verbose_name='схема сертификации',
        on_delete=CASCADE
    )
    applicant_representative_who_doing_application = ForeignKey(
        Signatory,
        related_name='representative_to_projects',
        verbose_name='представитель заявителя',
        on_delete=CASCADE
    )
    prod_name = TextField(
        verbose_name='Наименование продукции'
    )
    tn_ved_keys = ManyToManyField(TnVedKey, through='ProjectTnVedKey')
    manufacturer = ForeignKey(
        Manufacturer,
        related_name='project',
        verbose_name='Изготовитель',
        on_delete=CASCADE
    )
    docs_with_application = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Предоставленные с заявкой документы'
    )
    additional_information = CharField(
        max_length=CHAR_FIELD_MAX_SIZE,
        verbose_name='Дополнительная информация'
    )
    application_decision_date = DateField(
        verbose_name='Дата решения по заявке'
    )
    first_expert = ForeignKey(
        Expert,
        related_name='first_expert_to_project',
        verbose_name='Первый эксперт',
        on_delete=CASCADE
    )
    second_expert = ForeignKey(
        Expert,
        related_name='second_expert_to_project',
        verbose_name='Второй эксперт',
        on_delete=CASCADE
    )
    certificate_expert = ForeignKey(
        Expert,
        related_name='cert_expert_to_project',
        verbose_name='Эксперт в сертификате',
        on_delete=CASCADE
    )
    product_evaluation_work_plan_date = DateField(
        verbose_name='Дата плана работ по оценке'
    )
    certification_body_head = ForeignKey(
        Head,
        related_name='project',
        verbose_name='Руководитель в сертификате',
        on_delete=CASCADE
    )
    expert_opinion_date = DateField(
        verbose_name='Дата заключения эксперта'
    )
    release_decision_date = DateField(
        verbose_name='Дата решения о выдаче'
    )
    certificate_issue_date = DateField(
        verbose_name='Дата заключения эксперта'
    )
    certificate_expiry_date = DateField(
        verbose_name='Дата выдачи сертификата'
    )
    certificate_number = CharField(
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер сертификата'
    )
    certificate_application_1_form_number = CharField(
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер формы приложения 1 к сертификату'
    )
    certificate_application_2_form_number = CharField(
        max_length=CHAR_FIELD_PHONE_SIZE,
        verbose_name='Номер формы приложения 2 к сертификату'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProjectTnVedKey(Model):
    project = ForeignKey(
        Project,
        related_name='project_key',
        verbose_name='проект',
        on_delete=CASCADE,
    )
    key = ForeignKey(
        TnVedKey,
        related_name='key_project',
        verbose_name='ключ ТН ВЭД',
        on_delete=CASCADE,
    )

    def __str__(self):
        return f'{self.project} -  {self.key}'

    class Meta:
        ordering = ['key']
