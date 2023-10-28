from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from . import models


class BoardFilter(django_filters.FilterSet):
    # 이렇게 하면 foreign key까지 filter를 걸 수 있다.
    name = django_filters.CharFilter(field_name="author__username", lookup_expr="exact")
    name__icontains = django_filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )

    class Meta:
        model = models.Board
        fields = [
            "name",
            "name__icontains",
        ]
