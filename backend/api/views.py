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
    Protocol,
    Proxy,
    Reglament,
    Schem,
    Signatory,
    Standard,
    TnVedKey,
    Work,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

User = get_user_model()


class QMSViewSet(ModelViewSet):
    queryset = QMS.objects.all()
    serializer_class = QMSSerializer


class AgreementViewSet(ModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer


class ApplicantViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


class ApplicantInformationViewSet(ModelViewSet):
    queryset = ApplicantInformation.objects.all()
    serializer_class = ApplicantInformationSerializer


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class ProtocolViewSet(ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer


class CertificationBodyViewSet(ModelViewSet):
    queryset = CertificationBody.objects.all()
    serializer_class = CertificationBodySerializer


class CertificationObjectViewSet(ModelViewSet):
    queryset = CertificationObject.objects.all()
    serializer_class = CertificationObjectSerializer


class ConfirmationDecisionViewSet(ModelViewSet):
    queryset = ConfirmationDecision.objects.all()
    serializer_class = ConfirmationDecisionSerializer


class ExpertViewSet(ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer


class HeadViewSet(ModelViewSet):
    queryset = Head.objects.all()
    serializer_class = HeadSerializer


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class ManufacturingCompaniesViewSet(ModelViewSet):
    queryset = ManufacturingCompanies.objects.all()
    serializer_class = ManufacturingCompaniesSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ApplicationStaffSerializer
        return ApplicationUserSerializer


class ProxyViewSet(ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer


class ReglamentViewSet(ModelViewSet):
    queryset = Reglament.objects.all()
    serializer_class = ReglamentSerializer


class SchemViewSet(ModelViewSet):
    queryset = Schem.objects.all()
    serializer_class = SchemSerializer


class SignatoryViewSet(ModelViewSet):
    queryset = Signatory.objects.all()
    serializer_class = SignatorySerializer


class StandardViewSet(ModelViewSet):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer


class TnVedKeyViewSet(ModelViewSet):
    queryset = TnVedKey.objects.all()
    serializer_class = TnVedKeySerializer
