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
    Project,
    Proxy,
    Reglament,
    Schem,
    Signatory,
    Standard,
    TnVedKey,
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


class ProjectsAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'certification_body__name',
        'application__number',
        'applicant__name',
        'standard__name',
        'reglament__name',
        'schem__name',
        'prod_name',
        'manufacturer__name'
    )
    list_filter = (
        'name',
        'certification_body',
        'application',
        'applicant',
        'standard',
        'reglament',
        'schem',
        'prod_name',
        'manufacturer'
    )
    list_display = (
        'name',
        'certification_body',
        'application',
        'applicant',
        'standard',
        'reglament',
        'schem',
        'prod_name',
        'manufacturer'
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Application)
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
admin.site.register(CertificationBody)
admin.site.register(Project, ProjectsAdmin)
