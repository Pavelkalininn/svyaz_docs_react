from django.contrib import (
    admin,
)
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.admin import (
    UserAdmin,
)

from .models import (
    QMS,
    Agreement,
    Applicant,
    ApplicantInformation,
    Application,
    CertificationBody,
    CertificationObject,
    ConfirmationDecision,
    Expert,
    Head,
    Manufacturer,
    ManufacturingCompanies,
    Pattern,
    Protocol,
    Proxy,
    Reglament,
    Schem,
    Signatory,
    Standard,
    TnVedKey,
    Work,
)

User = get_user_model()
admin.site.empty_value_display = '-значение не задано-'

UserAdmin.fieldsets += (('Extra Fields', {'fields': ('role', )}),)


class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    search_fields = ('username', 'email', 'first_name')
    list_filter = ('username', 'email', 'first_name', 'role')


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = (
        'certification_body__name',
        'applicant__name',
        'standard__name',
        'reglament__name',
        'schem__name',
        'prod_name',
        'manufacturer__name'
    )
    list_filter = (
        'certification_body',
        'applicant',
        'standard',
        'reglament',
        'schem',
        'prod_name',
        'manufacturer'
    )
    list_display = (
        'certification_body',
        'applicant',
        'standard',
        'reglament',
        'schem',
        'prod_name',
        'manufacturer'
    )


class WorksAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'application__certification_body__name',
        'number',
        'date',
        'application__applicant__name',
        'application__standard__name',
        'application__reglament__name',
        'application__schem__name',
        'application__prod_name',
        'application__manufacturer__name'
    )
    list_filter = (
        'name',
        'application__certification_body',
        'number',
        'application__applicant',
        'application__standard',
        'application__reglament',
        'application__schem',
        'application__prod_name',
        'application__manufacturer'
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Proxy)
admin.site.register(Signatory)
admin.site.register(Agreement)
admin.site.register(ApplicantInformation)
admin.site.register(Applicant)
admin.site.register(Standard)
admin.site.register(CertificationObject)
admin.site.register(Reglament)
admin.site.register(Schem)
admin.site.register(TnVedKey)
admin.site.register(ConfirmationDecision)
admin.site.register(ManufacturingCompanies)
admin.site.register(QMS)
admin.site.register(Manufacturer)
admin.site.register(Expert)
admin.site.register(Head)
admin.site.register(Protocol)
admin.site.register(CertificationBody)
admin.site.register(Work, WorksAdmin)
admin.site.register(Pattern)
