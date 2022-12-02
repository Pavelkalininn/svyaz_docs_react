# -*- coding: UTF-8 -*-
from api.const import (
    ACT_ANALYSIS_PRODUCTION,
    CERTIFICATION_DECISION,
    CONCLUSION_APPLICATION_ANALYZE,
    PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL,
    PRODUCT_EVALUATION_WORK_PLAN,
)
from api.filters import (
    AgreementFilter,
    ApplicantFilter,
    ApplicationFilter,
    ExpertFilter,
    ManufacturerFilter,
    ManufacturingCompanyFilter,
    ProtocolFilter,
    ProxyFilter,
    QMSFilter,
    SignatoryFilter,
    StandardFilter,
    TnVedKeyFilter,
    WorkFilter,
)
from api.permissions import (
    CreateOrReadOnly,
    IsStaffOnly,
    OwnerOnly,
    StaffOrReadOnly,
)
from api.serializers import (
    AgreementSerializer,
    ApplicantCreateSerializer,
    ApplicantInformationSerializer,
    ApplicantReadSerializer,
    ApplicationStaffSerializer,
    ApplicationUserSerializer,
    CertificationBodySerializer,
    CertificationObjectSerializer,
    ConfirmationDecisionSerializer,
    ExpertSerializer,
    HeadSerializer,
    ManufacturerSerializer,
    ManufacturingCompanySerializer,
    PatternSerializer,
    ProtocolSerializer,
    ProxySerializer,
    QMSSerializer,
    ReglamentSerializer,
    SchemSerializer,
    SignatorySerializer,
    StandardSerializer,
    TnVedKeySerializer,
    WorkSerializer,
)
from api.utils import (
    document_creator,
)
from django.contrib.auth import (
    get_user_model,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from documents.models import (
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
    ManufacturingCompany,
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
from rest_framework.decorators import (
    action,
)
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import (
    SAFE_METHODS,
)
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
)

User = get_user_model()


class QMSViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = QMSSerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QMSFilter
    filterset_fields = ('number',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return QMS.objects.all()
        return self.request.user.qms

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class AgreementViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = AgreementSerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AgreementFilter
    filterset_fields = ('number',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Agreement.objects.all()
        return self.request.user.agreements

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ApplicantViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ApplicantFilter
    filterset_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ApplicantReadSerializer
        return ApplicantCreateSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Applicant.objects.all()
        return self.request.user.owner_applicants

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ApplicantInformationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ApplicantInformationSerializer
    permission_classes = (OwnerOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return ApplicantInformation.objects.all()
        return self.request.user.applicant_informations

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (IsStaffOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WorkFilter
    filterset_fields = ('name', 'number')

    @action(
        methods=['get'],
        permission_classes=(IsStaffOnly,),
        detail=True,
    )
    def download_conclusion_application_analise(self, request, pk):
        return document_creator(CONCLUSION_APPLICATION_ANALYZE, pk)

    @action(
        methods=['get'],
        permission_classes=(IsStaffOnly,),
        detail=True,
    )
    def download_certification_decision(self, request, pk):
        return document_creator(CERTIFICATION_DECISION, pk)

    @action(
        methods=['get'],
        permission_classes=(IsStaffOnly,),
        detail=True,
    )
    def download_product_evaluation_work_plan(self, request, pk):
        return document_creator(PRODUCT_EVALUATION_WORK_PLAN, pk)

    @action(
        methods=['get'],
        permission_classes=(IsStaffOnly,),
        detail=True,
    )
    def download_preliminary_analysis_production_protocol(self, request, pk):
        return document_creator(PRELIMINARY_ANALYSIS_PRODUCTION_PROTOCOL, pk)

    @action(
        methods=['get'],
        permission_classes=(IsStaffOnly,),
        detail=True,
    )
    def download_act_analysis_production(self, request, pk):
        return document_creator(ACT_ANALYSIS_PRODUCTION, pk)


class ProtocolViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ProtocolSerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProtocolFilter
    filterset_fields = ('number',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Protocol.objects.all()
        return self.request.user.protocols

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class CertificationBodyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = CertificationBody.objects.all()
    serializer_class = CertificationBodySerializer
    permission_classes = (StaffOrReadOnly,)


class CertificationObjectViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = CertificationObject.objects.all()
    serializer_class = CertificationObjectSerializer
    permission_classes = (CreateOrReadOnly,)


class ConfirmationDecisionViewSet(ModelViewSet):
    serializer_class = ConfirmationDecisionSerializer
    permission_classes = (OwnerOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return ConfirmationDecision.objects.all()
        return self.request.user.confirmation_decisions

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ExpertViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = (IsStaffOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ExpertFilter
    filterset_fields = ('full_name',)


class HeadViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Head.objects.all()
    serializer_class = HeadSerializer
    permission_classes = (IsStaffOnly,)


class ManufacturerViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ManufacturerSerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManufacturerFilter
    filterset_fields = ('search',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Manufacturer.objects.all()
        return self.request.user.manufacturers

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ManufacturingCompanyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ManufacturingCompanySerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManufacturingCompanyFilter
    filterset_fields = ('search',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return ManufacturingCompany.objects.all()
        return self.request.user.manufacturing_companies

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ApplicationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ApplicationFilter
    filterset_fields = ('search',)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ApplicationStaffSerializer
        return ApplicationUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all()
        return self.request.user.applications

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ProxyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ProxySerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProxyFilter
    filterset_fields = ('name',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Proxy.objects.all()
        return self.request.user.proxies

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class ReglamentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Reglament.objects.all()
    serializer_class = ReglamentSerializer
    permission_classes = (CreateOrReadOnly,)


class SchemViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Schem.objects.all()
    serializer_class = SchemSerializer
    permission_classes = (CreateOrReadOnly,)


class SignatoryViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = SignatorySerializer
    permission_classes = (OwnerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SignatoryFilter
    filterset_fields = ('full_name',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Signatory.objects.all()
        return self.request.user.signatories

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return serializer.save(
                owner=self.request.user
            )
        return serializer.save()


class StandardViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = (CreateOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StandardFilter
    filterset_fields = ('search',)


class TnVedKeyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = TnVedKey.objects.all()
    serializer_class = TnVedKeySerializer
    permission_classes = (CreateOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TnVedKeyFilter
    filterset_fields = ('name',)


class PatternViewSet(ModelViewSet):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    permission_classes = (IsStaffOnly,)
