from django.apps import AppConfig


class CustomPermissionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.custom_permission"
