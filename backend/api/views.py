from api.permissions import (
    CreateOrReadOnly,
    IsStaffOnly,
    OwnerOnly,
    StaffOrReadOnly,
)
from api.serializers import (
    AgreementSerializer,
    ApplicantInformationSerializer,
    ApplicantSerializer,
    ApplicationStaffSerializer,
    ApplicationUserSerializer,
    CertificationBodySerializer,
    CertificationObjectSerializer,
    ConfirmationDecisionSerializer,
    ExpertSerializer,
    HeadSerializer,
    ManufacturerSerializer,
    ManufacturingCompaniesSerializer,
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
from django.contrib.auth import (
    get_user_model,
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
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
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

    def get_queryset(self):
        if self.request.user.is_staff:
            return QMS.objects.filter(
                manufacturer__owner__owner_applicants=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return QMS.objects.filter(manufacturer__owner=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class AgreementViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = AgreementSerializer
    permission_classes = (OwnerOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Agreement.objects.filter(
                applicant_information__applicant=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return Agreement.objects.filter(
            applicant_information__applicant__owner=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class ApplicantViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ApplicantSerializer
    permission_classes = (OwnerOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Applicant.objects.filter(
                pk=self.kwargs.get('applicant_id')
            ).all()
        return Applicant.objects.filter(owner=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


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
            return ApplicantInformation.objects.filter(
                applicant=self.kwargs.get('applicant_id')
            ).all()
        return ApplicantInformation.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (IsStaffOnly,)


class ProtocolViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ProtocolSerializer
    permission_classes = (OwnerOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Protocol.objects.all()
        return Protocol.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class CertificationBodyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = CertificationBody.objects.all()
    serializer_class = CertificationBodySerializer
    permission_classes = (StaffOrReadOnly, )


class CertificationObjectViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = CertificationObject.objects.all()
    serializer_class = CertificationObjectSerializer
    permission_classes = (CreateOrReadOnly, )


class ConfirmationDecisionViewSet(ModelViewSet):
    serializer_class = ConfirmationDecisionSerializer
    permission_classes = (OwnerOnly, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return ConfirmationDecision.objects.filter(
                qms__manufacturer__owner__owner_applicants=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return ConfirmationDecision.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class ExpertViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = (IsStaffOnly, )


class HeadViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Head.objects.all()
    serializer_class = HeadSerializer
    permission_classes = (IsStaffOnly, )


class ManufacturerViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ManufacturerSerializer
    permission_classes = (OwnerOnly, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return Manufacturer.objects.filter(
                owner__owner_applicants=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return Manufacturer.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class ManufacturingCompaniesViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ManufacturingCompaniesSerializer
    permission_classes = (OwnerOnly, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return ManufacturingCompanies.objects.filter(
                owner__owner_applicants=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return ManufacturingCompanies.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class ApplicationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    permission_classes = (OwnerOnly, )

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ApplicationStaffSerializer
        return ApplicationUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.filter(
                applicant=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return Application.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class ProxyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = ProxySerializer
    permission_classes = (OwnerOnly, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return Proxy.objects.filter(
                signatory__applicant=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return Proxy.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class ReglamentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Reglament.objects.all()
    serializer_class = ReglamentSerializer
    permission_classes = (CreateOrReadOnly, )


class SchemViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Schem.objects.all()
    serializer_class = SchemSerializer
    permission_classes = (CreateOrReadOnly, )


class SignatoryViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    serializer_class = SignatorySerializer
    permission_classes = (OwnerOnly, )

    def get_queryset(self):
        if self.request.user.is_staff:
            return Signatory.objects.filter(
                applicant=self.kwargs.get(
                    'applicant_id'
                )
            ).all()
        return Signatory.objects.filter(
            owner=self.request.user
        ).all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class StandardViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = (CreateOrReadOnly, )


class TnVedKeyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset = TnVedKey.objects.all()
    serializer_class = TnVedKeySerializer
    permission_classes = (CreateOrReadOnly, )


class PatternViewSet(ModelViewSet):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    permission_classes = (IsStaffOnly, )
