from django.core.validators import RegexValidator
from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    FilePathField,
    Model,
    CASCADE,
    PositiveBigIntegerField,
    DO_NOTHING,
)

from backend.backend.settings import (
    INITIALS_REGEX,
    FULL_NAME_REGEX,
    PHONE_REGEX,
    EMAIL_REGEX,
    GTIN_REGEX,
)


class Application(Model):
    number = CharField(
        max_length=256,
        verbose_name='Номер заявки'
    )
    date = DateField(
        verbose_name='Дата заявки'
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['-application_date']


class Proxy(Model):
    name = CharField(
        max_length=256,
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
        max_length=150,
        verbose_name='Фамилия и инициалы',
        validators=(
            RegexValidator(
                regex=INITIALS_REGEX
            ),
        )
    )
    full_name = CharField(
        max_length=150,
        verbose_name='Полное фамилия имя отчество',
        validators=(
            RegexValidator(
                regex=FULL_NAME_REGEX
            ),
        )
    )
    position = CharField(
        max_length=150,
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
        max_length=150,
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
        max_length=250,
        verbose_name='адрес места нахождения заявителя'
    )
    applicant_work_location = CharField(
        max_length=250,
        verbose_name='адрес места осуществления деятельности заявителя'
    )
    phone_num = CharField(
        max_length=18,
        verbose_name='Номер телефона, начиная с "+"',
        validators=(
            RegexValidator(
                regex=PHONE_REGEX
            ),
        )
    )
    e_mail = CharField(
        max_length=40,
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
        max_length=256,
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
        max_length=256,
        verbose_name='Наименование стандарта'
    )
    voluntary_docs = CharField(
        max_length=256,
        verbose_name='Документы применяемые на добровольной основе'
    )
    requirement_name = CharField(
        max_length=256,
        verbose_name='Наименование требования'
    )
    short_requirement_name = CharField(
        max_length=256,
        verbose_name='Короткое наименование требования (только номер)'
    )
    requirement_modify_name = CharField(
        max_length=256,
        verbose_name='Наименование пунктов и таблиц из ТР ТС'
    )
    methods = CharField(
        max_length=256,
        verbose_name='Методы испытаний'
    )
    standard = CharField(
        max_length=256,
        verbose_name='стандарты!?'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CertificationObject(Model):
    name = CharField(
        max_length=30,
        verbose_name='объект сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Reglament(Model):
    name = CharField(
        max_length=30,
        verbose_name='регламент'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Schem(Model):
    name = CharField(
        max_length=30,
        verbose_name='схема сертификации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BaseProject(Model):
    name = CharField(
        max_length=256,
        verbose_name='Условное наименование работы'
    )
    application = ForeignKey(
        Application,
        related_name='project',
        verbose_name='заявка',
        on_delete=CASCADE
    )
    path_to_folder = FilePathField(
        verbose_name='путь к папке с работой',
    )
    applicant = ForeignKey(
        Applicant,
        related_name='project',
        verbose_name='заявитель',
        on_delete=CASCADE
    )
    signatory = ForeignKey(
        Signatory,
        related_name='project',
        verbose_name='подписант',
        on_delete=DO_NOTHING
    )
    standard = ForeignKey(
        Standard,
        related_name='project',
        verbose_name='стандарт',
        on_delete=CASCADE
    )
    GTIN_key = CharField(
        max_length=15,
        verbose_name='Код GTIN',
        validators=(
            RegexValidator(
                regex=GTIN_REGEX
            ),
        )
    )
    certification_object = ForeignKey(
        CertificationObject,
        related_name='project',
        verbose_name='объект сертификации',
        on_delete=CASCADE
    )
    reglament = ForeignKey(
        Reglament,
        related_name='project',
        verbose_name='регламент',
        on_delete=CASCADE
    )
    schem = ForeignKey(
        Schem,
        related_name='project',
        verbose_name='схема сертификации',
        on_delete=CASCADE
    )
    applicant_representative_who_doing_application = ForeignKey(
        Signatory,
        related_name='project',
        verbose_name='представитель заявителя',
        on_delete=CASCADE
    )
    prod_name = ForeignKey(
        Schem,
        related_name='project',
        verbose_name='наименование продукции',
        on_delete=CASCADE
    )
    tn_ved_keys: big_positive_integer
    qms_certificate
    docs_with_application
    additional_information
    application_decision_date
    first_expert
    second_expert
    certificate_expert
    product_evaluation_work_plan_date
    certification_body_head
    expert_opinion_date
    release_decision_date
    cerificate_issue_date
    certificate_expiry_date
    certificate_number
    cerificate_application_1_form_number
    cerificate_application_2_form_number

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
