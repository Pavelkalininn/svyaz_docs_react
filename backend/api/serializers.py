from django.contrib.auth import (
    get_user_model,
)
from djoser.serializers import (
    UserSerializer,
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
from rest_framework.fields import (
    CurrentUserDefault,
)
from rest_framework.serializers import (
    ModelSerializer,
)

User = get_user_model()


class QMSSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = QMS


class AgreementSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Agreement


class ApplicantInformationSerializer(ModelSerializer):
    agreements = AgreementSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'agreements',
            'ogrn',
            'inn',
            'applicant_location',
            'applicant_work_location',
            'phone_num',
            'e_mail',
            'date_issue',
            'date_expiry',
            'applicant',
            'owner'
        )
        model = ApplicantInformation


class ProxySerializer(ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'date_issue',
            'date_expiry',
            'owner'
        )
        model = Proxy


class SignatorySerializer(ModelSerializer):
    proxies = ProxySerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Signatory


class ApplicantSerializer(ModelSerializer):
    informations = ApplicantInformationSerializer(many=True)
    signatories = SignatorySerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'informations', 'signatories')
        model = Applicant


class CertificationBodySerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CertificationBody


class CertificationObjectSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CertificationObject


class ConfirmationDecisionSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ConfirmationDecision


class ExpertSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Expert


class HeadSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Head


class ManufacturerSerializer(ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'location',
            'work_location',
            'country',
            'qms',
            'manufacturing_companies'
        )
        model = Manufacturer


class ManufacturingCompanySerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ManufacturingCompany


class ApplicationUserSerializer(ModelSerializer):
    owner = UserSerializer(default=CurrentUserDefault(), read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'certification_body',
            'application',
            'applicant',
            'signatory',
            'standard',
            'GTIN_key',
            'certification_object',
            'reglament',
            'schem',
            'applicant_representative_who_doing_application',
            'prod_name',
            'tn_ved_keys',
            'manufacturer',
            'manufacturing_companies',
            'qms',
            'docs_with_application',
            'additional_information',
            'owner',
        )
        model = Application


class ApplicationStaffSerializer(ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'certification_body',
            'application',
            'path_to_folder',
            'applicant',
            'signatory',
            'standard',
            'GTIN_key',
            'certification_object',
            'reglament',
            'schem',
            'applicant_representative_who_doing_application',
            'prod_name',
            'tn_ved_keys',
            'manufacturer',
            'manufacturing_companies',
            'qms',
            'docs_with_application',
            'additional_information',
            'application_decision_date',
            'first_expert',
            'second_expert',
            'certificate_expert',
            'product_evaluation_work_plan_date',
            'certification_body_head',
            'expert_opinion_date',
            'release_decision_date',
            'certificate_issue_date',
            'certificate_expiry_date',
            'certificate_number',
            'certificate_application_1_form_number',
            'certificate_application_2_form_number',
            'owner',
        )
        model = Application


class ReglamentSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Reglament


class SchemSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Schem


class StandardSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Standard


class TnVedKeySerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = TnVedKey


class WorkSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Work


class ProtocolSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Protocol


class PatternSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Pattern
