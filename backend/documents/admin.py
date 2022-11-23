from django.contrib import admin

from .models import (
    User,
    Application,
    Proxy,
    Signatory,
    Agreement,
    ApplicantInformation,
    Applicant,
    Standard,
    CertificationObject,
    Reglament,
    Schem,
    TnVedKey,
    ConfirmationDecision,
    ManufacturingCompanies,
    QMS,
    Manufacturer,
    Expert,
    Head,
    CertificationBody,
    Project,
    ProjectTnVedKey,
)

EMPTY_VALUE = 'значение не задано'

admin.site.register(User)
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
admin.site.register(Project)
admin.site.register(ProjectTnVedKey)
