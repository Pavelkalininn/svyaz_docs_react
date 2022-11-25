from api.views import (
    AgreementViewSet,
    ApplicantInformationViewSet,
    ApplicantViewSet,
    ApplicationViewSet,
    CertificationBodyViewSet,
    CertificationObjectViewSet,
    ConfirmationDecisionViewSet,
    ExpertViewSet,
    HeadViewSet,
    ManufacturerViewSet,
    ManufacturingCompaniesViewSet,
    ProtocolViewSet,
    ProxyViewSet,
    QMSViewSet,
    ReglamentViewSet,
    SchemViewSet,
    SignatoryViewSet,
    StandardViewSet,
    TnVedKeyViewSet,
    WorkViewSet,
)
from django.urls import (
    include,
    path,
)
from rest_framework import (
    routers,
)

router = routers.DefaultRouter()

router.register('tn_ved_keys', TnVedKeyViewSet, basename='tn_ved_key-list')
router.register('standards', StandardViewSet, basename='standard-list')
router.register('signatories', SignatoryViewSet, basename='signatory-list')
router.register('schems', SchemViewSet, basename='schem-list')
router.register('reglaments', ReglamentViewSet, basename='reglament-list')

router.register(
    'proxies',
    ProxyViewSet,
    basename='proxy-list'
)
router.register(
    'applications',
    ApplicationViewSet,
    basename='application-list'
)
router.register(
    'manufacturing_companies',
    ManufacturingCompaniesViewSet,
    basename='manufacturing_company-list'
)
router.register(
    'manufacturers',
    ManufacturerViewSet,
    basename='manufacturer-list'
)
router.register(
    'heads',
    HeadViewSet,
    basename='head-list'
)

router.register(
    'experts',
    ExpertViewSet,
    basename='expert-list'
)
router.register(
    'confirmation_decisions',
    ConfirmationDecisionViewSet,
    basename='confirmation_decision-list'
)
router.register(
    'certification_objects',
    CertificationObjectViewSet,
    basename='certification_object-list'
)
router.register(
    'certification_bodies',
    CertificationBodyViewSet,
    basename='certification_body-list'
)
router.register(
    'works',
    WorkViewSet,
    basename='work-list'
)

router.register(
    'applicant_information',
    ApplicantInformationViewSet,
    basename='applicant_information-list'
)
router.register(
    'applicants',
    ApplicantViewSet,
    basename='applicant-list'
)
router.register(
    'agreements',
    AgreementViewSet,
    basename='agreement-list'
)
router.register(
    'protocols',
    ProtocolViewSet,
    basename='protocol-list'
)
router.register('qms', QMSViewSet, basename='qms-list')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
