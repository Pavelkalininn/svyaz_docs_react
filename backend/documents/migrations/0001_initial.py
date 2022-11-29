# Generated by Django 3.2.16 on 2022-11-29 10:40

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import (
    settings,
)
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex='^[\\w.@+-]+\\Z')], verbose_name='Логин')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('role', models.CharField(choices=[('user', 'USER'), ('staff', 'STAFF'), ('admin', 'ADMIN')], default='user', max_length=16, verbose_name='Роль')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('-id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование заявителя')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_applicants', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Заявитель',
                'verbose_name_plural': 'Заявители',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GTIN_key', models.CharField(blank=True, max_length=18, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{8,14}\\Z')], verbose_name='Код GTIN')),
                ('prod_name', models.TextField(verbose_name='Наименование продукции')),
                ('docs_with_application', models.TextField(verbose_name='Предоставленные с заявкой документы')),
                ('additional_information', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительная информация')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.applicant', verbose_name='заявитель')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CertificationBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование органа')),
                ('attestation', models.CharField(max_length=127, verbose_name='Аттестат аккредитации')),
                ('attestation_date', models.DateField(verbose_name='Дата выдачи аттестата')),
            ],
            options={
                'verbose_name': 'Орган по сертификации продукции',
                'verbose_name_plural': 'Органы по сертфикации продукции',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CertificationObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='объект сертификации')),
            ],
            options={
                'verbose_name': 'Объект сертификации',
                'verbose_name_plural': 'Объекты сертификации',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.(?:[A-ZА-ЯЁ]\\.|)\\Z')], verbose_name='Фамилия и инициалы эксперта')),
                ('full_name', models.CharField(max_length=127, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ][a-zа-яё]+(?: [A-ZА-ЯЁ][a-zа-яё]+|)\\Z')], verbose_name='Полное фамилия имя отчество эксперта')),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experts', to='documents.certificationbody', verbose_name='Орган по сертификации')),
            ],
            options={
                'verbose_name': 'Эксперт',
                'verbose_name_plural': 'Эксперты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.(?:[A-ZА-ЯЁ]\\.|)\\Z')], verbose_name='Фамилия и инициалы руководителя')),
                ('full_name', models.CharField(max_length=127, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ][a-zа-яё]+(?: [A-ZА-ЯЁ][a-zа-яё]+|)\\Z')], verbose_name='Полное фамилия имя отчество руководителя')),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head', to='documents.certificationbody', verbose_name='Орган по сертификации')),
            ],
            options={
                'verbose_name': 'Руководитель органа',
                'verbose_name_plural': 'Руководители органов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование изготовителя')),
                ('location', models.CharField(max_length=255, verbose_name='Адрес места нахождения изготовителя')),
                ('work_location', models.CharField(max_length=255, verbose_name='Адрес места осуществления изготовителя')),
                ('country', models.CharField(max_length=40, verbose_name='Страна изготовления')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturers', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Изготовитель',
                'verbose_name_plural': 'Изготовители',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование формы')),
                ('date_issue', models.DateField(verbose_name='Дата начала использования')),
                ('file', models.FileField(unique=True, upload_to='patterns')),
            ],
            options={
                'verbose_name': 'Форма документа',
                'verbose_name_plural': 'Формы документов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255, verbose_name='Номер протокола')),
                ('date', models.DateField(verbose_name='Дата протокола')),
                ('body_certificate', models.CharField(max_length=40, verbose_name='Аттестат аккредитации испытательной лаборатории')),
                ('body_name', models.CharField(max_length=255, verbose_name='Полное наименование лаборатории в родительном падеже (испытательной лабораторией ...)')),
                ('signatory', models.CharField(blank=True, max_length=127, null=True, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.(?:[A-ZА-ЯЁ]\\.|)\\Z')], verbose_name='Фамилия и инициалы руководителя ИЛ в протоколе')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='protocols', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Протокол',
                'verbose_name_plural': 'Протоколы',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Reglament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, verbose_name='регламент')),
            ],
            options={
                'verbose_name': 'Регламент',
                'verbose_name_plural': 'Регламенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Schem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='схема сертификации')),
            ],
            options={
                'verbose_name': 'Схема сертификации',
                'verbose_name_plural': 'Схемы сертификации',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование стандарта')),
                ('voluntary_docs', models.CharField(max_length=255, unique=True, verbose_name='Документы применяемые на добровольной основе')),
                ('requirement_name', models.CharField(max_length=255, unique=True, verbose_name='Наименование требования')),
                ('short_requirement_name', models.CharField(max_length=255, unique=True, verbose_name='Короткое наименование требования (только номер)')),
                ('requirement_modify_name', models.CharField(max_length=255, unique=True, verbose_name='Наименование пунктов и таблиц из ТР ТС')),
                ('methods', models.CharField(blank=True, max_length=255, null=True, verbose_name='Методы испытаний')),
                ('standard', models.CharField(blank=True, max_length=255, null=True, verbose_name='стандарты!?')),
            ],
            options={
                'verbose_name': 'Стандарт',
                'verbose_name_plural': 'Стандарты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TnVedKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveBigIntegerField(unique=True, verbose_name='Код ТН ВЭД ЕАЭС')),
                ('description', models.CharField(max_length=255, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Код ТН ВЭД ЕАЭС',
                'verbose_name_plural': 'Коды ТН ВЭД ЕАЭС',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Условное наименование работы')),
                ('path_to_folder', models.CharField(max_length=255, verbose_name='путь к папке с работой')),
                ('number', models.CharField(max_length=255, unique=True, verbose_name='Номер заявки')),
                ('date', models.DateField(verbose_name='Дата заявки')),
                ('application_decision_date', models.DateField(blank=True, null=True, verbose_name='Дата решения по заявке')),
                ('product_evaluation_work_plan_date', models.DateField(blank=True, null=True, verbose_name='Дата плана работ по оценке')),
                ('expert_opinion_date', models.DateField(blank=True, null=True, verbose_name='Дата заключения эксперта')),
                ('release_decision_date', models.DateField(blank=True, null=True, verbose_name='Дата решения о выдаче')),
                ('certificate_issue_date', models.DateField(blank=True, null=True, verbose_name='Дата заключения эксперта')),
                ('certificate_expiry_date', models.DateField(blank=True, null=True, verbose_name='Дата выдачи сертификата')),
                ('certificate_number', models.CharField(blank=True, max_length=18, null=True, verbose_name='Номер сертификата')),
                ('certificate_application_1_form_number', models.CharField(blank=True, max_length=18, null=True, verbose_name='Номер формы приложения 1 к сертификату')),
                ('certificate_application_2_form_number', models.CharField(blank=True, max_length=18, null=True, verbose_name='Номер формы приложения 2 к сертификату')),
                ('application_registration_form_notes', models.CharField(blank=True, max_length=40, null=True, verbose_name='Примечания по регистрации заявки (в форму регистрации заявок)')),
                ('registry_certificate_confirmation_notes', models.CharField(blank=True, max_length=40, null=True, verbose_name='Примечания о выдаче сертификата (в форму регистрации заявок)')),
                ('sampling_identification_with_dt', models.CharField(blank=True, max_length=40, null=True, verbose_name='Отбор образцов, заключение идентификации, дата (для Формы регистрации заявок)')),
                ('directing_with_dt', models.CharField(blank=True, max_length=40, null=True, verbose_name='№ направления в ИЛ, дата (для Формы регистрации заявок)')),
                ('conclusion_application_analyze_date', models.DateField(blank=True, null=True, verbose_name='Дата заключения анализа заявки')),
                ('evaluation_planned_date', models.DateField(blank=True, null=True, verbose_name='Запланированный срок оценивания')),
                ('evaluation_analyze_planned_date', models.DateField(blank=True, null=True, verbose_name='Запланированный срок анализа результатов оценивания')),
                ('preliminary_analysis_production_protocol_date', models.DateField(blank=True, null=True, verbose_name='Дата протокола предварительного анализа производства')),
                ('act_analysis_production_date', models.DateField(blank=True, null=True, verbose_name='Дата акта анализа состояния производства')),
                ('analysis_production_duration_till_date', models.DateField(blank=True, null=True, verbose_name='Срок проведения анализа сотсояния производства (По)')),
                ('conclusion_of_conformity_assessment_date', models.DateField(blank=True, null=True, verbose_name='Дата заключения анализа')),
                ('analysis_production_registry_notes', models.DateField(blank=True, null=True, verbose_name='Примечания по регистрации анализа состояния продукции')),
                ('analysis_production_head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analysis_production_head_works', to='documents.expert', verbose_name='Руководитель комиссии')),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='work', to='documents.application', verbose_name='заявка')),
                ('application_analyze_expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_analyze_expert_works', to='documents.expert', verbose_name='Эксперт в заключении анализа')),
                ('certificate_expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_expert_works', to='documents.expert', verbose_name='Эксперт в сертификате')),
                ('certificate_head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_head_works', to='documents.head', verbose_name='Руководитель в сертификате')),
                ('conclusion_expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conclusion_expert_works', to='documents.expert', verbose_name='Эксперт в заключении')),
                ('decision_head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decision_head_works', to='documents.head', verbose_name='Руководитель ОС в решении о проведении')),
                ('evaluation_analyze_expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_analyze_expert_works', to='documents.expert', verbose_name='Эксперт по анализу результатов оценивания')),
                ('evaluation_expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_expert_works', to='documents.expert', verbose_name='Эксперт ответственный за оценивание')),
                ('protocols', models.ManyToManyField(to='documents.Protocol', verbose_name='Протоколы испытаний полученные в ходе сертификации')),
            ],
            options={
                'verbose_name': 'Работа органа',
                'verbose_name_plural': 'Работы органа',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Signatory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=127, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.(?:[A-ZА-ЯЁ]\\.|)\\Z')], verbose_name='Фамилия и инициалы')),
                ('full_name', models.CharField(max_length=127, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ][a-zа-яё]+(?: [A-ZА-ЯЁ][a-zа-яё]+|)\\Z')], verbose_name='Полное фамилия имя отчество')),
                ('position', models.CharField(max_length=127, verbose_name='Должность')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatories', to='documents.applicant', verbose_name='заявитель')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatories', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Подписант',
                'verbose_name_plural': 'Подписанты',
                'ordering': ['short_name'],
            },
        ),
        migrations.CreateModel(
            name='QMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255, unique=True, verbose_name='Номер сертификата СМК')),
                ('date_issue', models.DateField(verbose_name='Дата выдачи')),
                ('date_expiry', models.DateField(verbose_name='Дата окончания действия')),
                ('body_certificate', models.CharField(max_length=40, verbose_name='Аттестат аккредитации органа по сертификации СМК')),
                ('body_name', models.CharField(max_length=255, verbose_name='Наименование органа по сертификации СМК')),
                ('signatory', models.CharField(blank=True, max_length=127, null=True, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.(?:[A-ZА-ЯЁ]\\.|)\\Z')], verbose_name='Фамилия и инициалы эксперта в сертификате СМК')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qms', to='documents.manufacturer', verbose_name='Изготовитель')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qms', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Сертификат СМК',
                'verbose_name_plural': 'Сертификаты СМК',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='номер/наименование')),
                ('date_issue', models.DateField(verbose_name='дата выдачи')),
                ('date_expiry', models.DateField(blank=True, null=True, verbose_name='дата окончания действия')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proxies', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
                ('signatory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proxies', to='documents.signatory', verbose_name='Подписант')),
            ],
            options={
                'verbose_name': 'Доверенность',
                'verbose_name_plural': 'Доверенности',
                'ordering': ['-date_issue'],
            },
        ),
        migrations.CreateModel(
            name='ManufacturingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование производственной площадки')),
                ('location', models.CharField(max_length=255, verbose_name='Место нахождения производственной площадки')),
                ('work_location', models.CharField(max_length=255, verbose_name='Место осуществления производственной площадки')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturing_companies', to='documents.manufacturer', verbose_name='Изготовитель')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturing_companies', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Производственная площадка',
                'verbose_name_plural': 'Производственные площадки',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ConfirmationDecision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=127, unique=True, verbose_name='Наименование решения о подтверждении СМК')),
                ('date', models.DateField(verbose_name='Дата решения о подтверждении СМК')),
                ('signatory', models.CharField(blank=True, max_length=127, null=True, validators=[django.core.validators.RegexValidator(regex='^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.(?:[A-ZА-ЯЁ]\\.|)\\Z')], verbose_name='Фамилия и инициалы эксперта в решении о подтверждении')),
                ('qms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_decision', to='documents.qms', verbose_name='Сертификат СМК')),
            ],
            options={
                'verbose_name': 'Решение о подтверждении СМК',
                'verbose_name_plural': 'Решения о подтверждении СМК',
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='application',
            name='applicant_representative_who_doing_application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representative_to_applications', to='documents.signatory', verbose_name='представитель заявителя'),
        ),
        migrations.AddField(
            model_name='application',
            name='certification_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.certificationbody', verbose_name='Орган по сертификации'),
        ),
        migrations.AddField(
            model_name='application',
            name='certification_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.certificationobject', verbose_name='объект сертификации'),
        ),
        migrations.AddField(
            model_name='application',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.manufacturer', verbose_name='Изготовитель'),
        ),
        migrations.AddField(
            model_name='application',
            name='manufacturing_companies',
            field=models.ManyToManyField(related_name='applications', to='documents.ManufacturingCompany', verbose_name='Производственные площадки'),
        ),
        migrations.AddField(
            model_name='application',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='application',
            name='protocols',
            field=models.ManyToManyField(to='documents.Protocol', verbose_name='Протоколы испытаний приложенные к заявке'),
        ),
        migrations.AddField(
            model_name='application',
            name='qms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.qms', verbose_name='Сертификат СМК'),
        ),
        migrations.AddField(
            model_name='application',
            name='reglament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.reglament', verbose_name='регламент'),
        ),
        migrations.AddField(
            model_name='application',
            name='schem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.schem', verbose_name='схема сертификации'),
        ),
        migrations.AddField(
            model_name='application',
            name='signatory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='applications', to='documents.signatory', verbose_name='подписант'),
        ),
        migrations.AddField(
            model_name='application',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='documents.standard', verbose_name='стандарт'),
        ),
        migrations.AddField(
            model_name='application',
            name='tn_ved_keys',
            field=models.ManyToManyField(related_name='applications', to='documents.TnVedKey'),
        ),
        migrations.CreateModel(
            name='ApplicantInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ogrn', models.PositiveBigIntegerField(verbose_name='ОГРН')),
                ('inn', models.PositiveBigIntegerField(verbose_name='ИНН')),
                ('applicant_location', models.CharField(max_length=255, verbose_name='адрес места нахождения заявителя')),
                ('applicant_work_location', models.CharField(max_length=255, verbose_name='адрес места осуществления деятельности заявителя')),
                ('phone_num', models.CharField(max_length=18, validators=[django.core.validators.RegexValidator(regex='^\\+[0-9]{10,18}\\Z')], verbose_name='Номер телефона, начиная с "+"')),
                ('e_mail', models.CharField(max_length=40, validators=[django.core.validators.RegexValidator(regex='^.{2,}@.{2,}\\..{2,}\\Z')], verbose_name='e-mail')),
                ('date_issue', models.DateField(verbose_name='дата начала актуальности этих документов')),
                ('date_expiry', models.DateField(blank=True, null=True, verbose_name='дата окончания актуальности этих документов')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informations', to='documents.applicant', verbose_name='Заявитель')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_informations', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Карточка организации',
                'verbose_name_plural': 'Карточки организации',
                'ordering': ['-date_issue'],
            },
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=127, unique=True, verbose_name='Номер соглашения')),
                ('date_issue', models.DateField(verbose_name='Дата соглашения')),
                ('date_expiry', models.DateField(blank=True, null=True, verbose_name='Срок действия')),
                ('applicant_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='documents.applicantinformation', verbose_name='параметры заявителя')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Соглашение',
                'verbose_name_plural': 'Соглашения',
                'ordering': ['-date_issue'],
            },
        ),
        migrations.AddConstraint(
            model_name='signatory',
            constraint=models.UniqueConstraint(fields=('short_name', 'position'), name='unique_signatory'),
        ),
        migrations.AddConstraint(
            model_name='protocol',
            constraint=models.UniqueConstraint(fields=('number', 'owner'), name='unique_applicant_protocol'),
        ),
        migrations.AddConstraint(
            model_name='manufacturingcompany',
            constraint=models.UniqueConstraint(fields=('name', 'location', 'work_location'), name='unique_manufacturing_companies'),
        ),
        migrations.AddConstraint(
            model_name='manufacturer',
            constraint=models.UniqueConstraint(fields=('name', 'location', 'work_location'), name='unique_manufacturer'),
        ),
        migrations.AddConstraint(
            model_name='applicantinformation',
            constraint=models.UniqueConstraint(fields=('ogrn', 'date_issue'), name='unique_applicant_information'),
        ),
    ]
