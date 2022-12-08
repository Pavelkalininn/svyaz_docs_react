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
    SerializerMethodField,
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


class ApplicantCreateSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'informations', 'signatories', 'owner')
        model = Applicant


class ApplicantReadSerializer(ApplicantCreateSerializer):
    informations = ApplicantInformationSerializer(many=True)
    signatories = SignatorySerializer(many=True)

    class Meta(ApplicantCreateSerializer.Meta):
        ...


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
    class Meta:
        fields = (
            'id',
            'certification_body',
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
            'applicant',
            'certification_body',
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
            'protocols',
            'qms',
            'docs_with_application',
            'additional_information',
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
    conclusion_application_analyze_available = SerializerMethodField()
    application_decision_available = SerializerMethodField()
    product_evaluation_work_plan_available = SerializerMethodField()
    preliminary_analysis_production_protocol_available = SerializerMethodField(
    )
    act_analysis_production_available = SerializerMethodField()
    expert_opinion_available = SerializerMethodField()
    conclusion_of_conformity_assessment_available = SerializerMethodField()
    release_decision_available = SerializerMethodField()
    certificate_issue_available = SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Work

    # self.work.act_analysis_production_date
    @staticmethod
    def get_conclusion_application_analyze_available(obj) -> bool:
        return bool(
            obj.number
            and obj.conclusion_application_analyze_date
            and obj.date
            and obj.application_analyze_expert
        )

    @staticmethod
    def get_application_decision_available(obj) -> bool:
        return bool(
            obj.number
            and obj.date
            and obj.application_decision_date
            and obj.decision_head
            and obj.conclusion_expert
        )

    @staticmethod
    def get_product_evaluation_work_plan_available(obj) -> bool:
        return bool(
            obj.decision_head
            and obj.product_evaluation_work_plan_date
            and obj.number
            and obj.release_decision_date
            and obj.evaluation_expert
            and obj.evaluation_planned_date
            and obj.evaluation_analyze_expert
            and obj.evaluation_analyze_planned_date
            and obj.conclusion_expert
        )

    @staticmethod
    def get_preliminary_analysis_production_protocol_available(obj) -> bool:
        return bool(
            obj.preliminary_analysis_production_protocol_date
            and obj.number
            and obj.conclusion_expert.name
        )

    @staticmethod
    def get_act_analysis_production_available(obj) -> bool:
        return bool(
            obj.act_analysis_production_date
            and obj.analysis_production_duration_till_date
            and obj.number
            and obj.date
            and obj.analysis_production_head
        )

    @staticmethod
    def get_expert_opinion_available(obj) -> bool:
        return bool(
            obj.number
            and obj.expert_opinion_date
            and obj.application_analyze_expert
            and obj.date
            and obj.act_analysis_production_date
        )

    @staticmethod
    def get_conclusion_of_conformity_assessment_available(obj) -> bool:
        return bool(
            obj.number
            and obj.conclusion_of_conformity_assessment_date
            and obj.application_decision_date
            and obj.conclusion_expert
            and obj.act_analysis_production_date
        )

    @staticmethod
    def get_release_decision_available(obj) -> bool:
        return bool(
            obj.number
            and obj.release_decision_date
            and obj.conclusion_of_conformity_assessment_date
            and obj.certificate_expiry_date
            and obj.certificate_head
            and obj.act_analysis_production_date
        )

    @staticmethod
    def get_certificate_issue_available(obj) -> bool:
        return bool(
            obj.expert_opinion_date
            and obj.certificate_head
            and obj.certificate_expert
            and obj.act_analysis_production_date
        )


class ProtocolSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Protocol


class PatternSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Pattern
