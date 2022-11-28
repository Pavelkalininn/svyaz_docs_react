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
    PatternViewSet,
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
router.register('schems', SchemViewSet, basename='schem-list')
router.register('reglaments', ReglamentViewSet, basename='reglament-list')
router.register('heads', HeadViewSet, basename='head-list')
router.register('experts', ExpertViewSet, basename='expert-list')
router.register('works', WorkViewSet, basename='work-list')

router.register(
    r'signatories/(?P<applicant_id>\d+)',
    SignatoryViewSet,
    basename='signatory-list'
)
router.register(
    r'proxies/(?P<applicant_id>\d+)',
    ProxyViewSet,
    basename='proxy-list'
)
router.register(
    r'applications/(?P<applicant_id>\d+)',
    ApplicationViewSet,
    basename='application-list'
)
router.register(
    r'manufacturing_companies/(?P<applicant_id>\d+)',
    ManufacturingCompaniesViewSet,
    basename='manufacturing_company-list'
)
router.register(
    r'manufacturers/(?P<applicant_id>\d+)',
    ManufacturerViewSet,
    basename='manufacturer-list'
)
router.register(
    r'confirmation_decisions/(?P<applicant_id>\d+)',
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
    r'applicant_information/(?P<applicant_id>\d+)',
    ApplicantInformationViewSet,
    basename='applicant_information-list'
)
router.register('applicants', ApplicantViewSet, basename='applicant-list')
router.register(
    r'agreements/(?P<applicant_id>\d+)',
    AgreementViewSet,
    basename='agreement-list'
)
router.register(
    r'protocols/(?P<applicant_id>\d+)',
    ProtocolViewSet,
    basename='protocol-list'
)
router.register(r'qms/(?P<applicant_id>\d+)', QMSViewSet, basename='qms-list')
router.register('patterns', PatternViewSet, basename='pattern-list')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
