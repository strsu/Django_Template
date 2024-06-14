from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import BadRequest

from api.common.admin import BaseAdmin
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

    def save_model(self, request, obj, form, change):
        # 할 일 정의
        if obj.pk:
            ## NOTE - 내가 만든 Code400Exception 같은 Exception은 django에서 500으로 인지하기 때문에 Handler400을 사용하려면 django에서 만든 400 Exception을 사용해야한다.
            ## [x] - Admin Page에서 수정하는 경우 해당 함수를 통해서 호출된다.
            ## Admin에서 기능을 막고 싶으면 여기서 하면 된다!!
            raise BadRequest("수정금지")
        return super(SoccerPlaceAdmin, self).save_model(request, obj, form, change)


class SoccerTimeInstanceInline(admin.TabularInline):
    model = SoccerTime


class SoccerWithInstanceInline(admin.TabularInline):
    model = SoccerWith


class SoccerAdmin(BaseAdmin):
    list_display = ("username", "validated_where_list", "when", "level_choice", "score")
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
        if obj.where:
            return obj.where.name if obj.where.name is not None else "-"
        return "-"

    # 겉에 보이는
    def level_choice(self, obj):
        custom_display = {
            Soccer.Level.RED: "빨강색",
            Soccer.Level.ORANGE: "주황색",
            Soccer.Level.YELLO: "노랑색",
            Soccer.Level.GREEN: "초록색",
            Soccer.Level.BLUE: "파랑색",
            Soccer.Level.INDIGO: "남색",
            Soccer.Level.PURPLE: "자주색",
            Soccer.Level.BLACK: "검정색",
            Soccer.Level.WHITE: "하얀색",
            Soccer.Level.GRAY: "회색",
        }
        return custom_display.get(obj.level)

    level_choice.short_description = "난이도"  # 컬럼 이름 설정

    # 안에 보이는
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "level":
            kwargs["choices"] = (
                (Soccer.Level.RED, "빨강색"),
                (Soccer.Level.ORANGE, "주황색"),
                (Soccer.Level.YELLO, "노랑색"),
                (Soccer.Level.GREEN, "초록색"),
                (Soccer.Level.BLUE, "파랑색"),
                (Soccer.Level.INDIGO, "남색"),
                (Soccer.Level.PURPLE, "자주색"),
                (Soccer.Level.BLACK, "검정색"),
                (Soccer.Level.WHITE, "하얀색"),
                (Soccer.Level.GRAY, "회색"),
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    # validated_where_list.admin_order_field = "where__name"
    # validated_where_list.short_description = "Soccer Name"


admin.site.register(Soccer, SoccerAdmin)
admin.site.register(SoccerPlace, SoccerPlaceAdmin)
