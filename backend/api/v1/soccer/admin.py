from django.contrib import admin
from django.utils.html import format_html

from api.v1.soccer.models import Soccer, SoccerTime, SoccerWith, SoccerPlace

# Register your models here.


class SoccerPlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude")
    list_filter = ("name", "address")

    search_fields = ("name__startswith", "address__startswith")
    ordering = ("name",)  # 여기서 ordering을 하면 admin내 모든 place가 ordering 된다.

    actions = ["make_published"]

    @admin.action(description="Mark selected stories as published")
    def make_published(self, request, queryset):
        queryset.update(name="p")


class SoccerTimeInstanceInline(admin.TabularInline):
    model = SoccerTime


class SoccerWithInstanceInline(admin.TabularInline):
    model = SoccerWith


class SoccerAdmin(admin.ModelAdmin):
    list_display = ("username", "validated_where_list", "when", "level", "score")
    list_display_links = ("username", "validated_where_list")

    inlines = [SoccerTimeInstanceInline, SoccerWithInstanceInline]

    @admin.display(ordering="user")
    def username(self, obj):
        # 이렇게 하면 장고 Admin에서 색상을 줄 수 있다.
        return format_html(
            '<span style="color: {};">{}</span>',
            "ORANGE",
            obj.user,
        )

    def validated_where_list(self, obj):
        return obj.where.name if obj.where.name is not None else "-"

    # validated_where_list.admin_order_field = "where__name"
    # validated_where_list.short_description = "Soccer Name"


admin.site.register(Soccer, SoccerAdmin)
admin.site.register(SoccerPlace, SoccerPlaceAdmin)
