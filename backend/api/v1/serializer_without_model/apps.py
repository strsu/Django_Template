from django.apps import AppConfig


class SerializerWithoutModelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.serializer_without_model"
