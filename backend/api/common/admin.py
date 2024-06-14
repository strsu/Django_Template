from django.contrib import admin

# Register your models here.


class BaseAdmin(admin.ModelAdmin):

    exclude = ("deleted_at",)  ## deleted_at 감추기

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(deleted_at__isnull=True)  ## 삭제된 자원은 안 보이도록
