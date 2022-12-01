import django_filters
from django.db.models import (
    Q,
)
from documents.models import (
    QMS,
    Agreement,
    Applicant,
    Application,
    Expert,
    Manufacturer,
    ManufacturingCompany,
    Protocol,
    Proxy,
    Signatory,
    Standard,
    TnVedKey,
    Work,
)


class QMSFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='number'
    )

    class Meta:
        model = QMS
        fields = ('number', )


class AgreementFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='number'
    )

    class Meta:
        model = Agreement
        fields = ('number', )


class ApplicantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name'
    )

    class Meta:
        model = Applicant
        fields = ('name', )


class WorkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name'
    )
    number = django_filters.CharFilter(
        lookup_expr='istartswith',
        field_name='number'
    )

    class Meta:
        model = Work
        fields = ('name', 'number')


class ProtocolFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='number'
    )

    class Meta:
        model = Protocol
        fields = ('number', )


class ExpertFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='full_name'
    )

    class Meta:
        model = Expert
        fields = ('full_name', )


class ManufacturerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label="search")

    class Meta:
        model = Manufacturer
        fields = ('search', )

    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            or Q(location__icontains=value)
            or Q(work_location__icontains=value)
        )


class ManufacturingCompanyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label="search")

    class Meta:
        model = ManufacturingCompany
        fields = ('search', )

    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            or Q(location__icontains=value)
            or Q(work_location__icontains=value)
        )


class ApplicationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label="search")

    class Meta:
        model = Application
        fields = ('search', )

    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(
            Q(prod_name__icontains=value)
            or Q(standard__name__icontains=value)
        )


class ProxyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name'
    )

    class Meta:
        model = Proxy
        fields = ('name', )


class SignatoryFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='full_name'
    )

    class Meta:
        model = Signatory
        fields = ('full_name', )


class StandardFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label="search")

    class Meta:
        model = Standard
        fields = ('search', )

    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            or Q(voluntary_docs__icontains=value)
            or Q(requirement_name__icontains=value)
        )


class TnVedKeyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='istartswith',
        field_name='name'
    )

    class Meta:
        model = TnVedKey
        fields = ('name', )
