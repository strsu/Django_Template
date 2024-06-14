from django.apps import AppConfig


class CeleryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.celery"

    def ready(self):
        import api.v1.celery.signals
