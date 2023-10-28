from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from . import models


class BoardFilter(django_filters.FilterSet):
    name__icontains = django_filters.CharFilter(
        field_name="infra__name", lookup_expr="icontains"
    )
    address__icontains = django_filters.CharFilter(
        field_name="infra__address", lookup_expr="icontains"
    )

    class Meta:
        model = models.Board
        fields = ["name__icontains", "address__icontains"]
