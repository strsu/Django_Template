from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from . import models


class BoardFilter(django_filters.FilterSet):
    # 이렇게 하면 foreign key까지 filter를 걸 수 있다.
    name = django_filters.CharFilter(
        field_name="author__username",
        lookup_expr="exact",
        help_text="`필터` - 저자명과 동일한",
    )
    name__icontains = django_filters.CharFilter(
        field_name="author__username",
        lookup_expr="icontains",
        help_text="`필터` - 저자명을 포함",
    )
    category = django_filters.CharFilter(
        field_name="category__name",
        lookup_expr="exact",
        help_text="`필터` - 선택한 카테고리",
    )

    class Meta:
        model = models.Board
        fields = ["name", "name__icontains", "category"]
