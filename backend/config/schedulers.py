from django_celery_beat.models import PeriodicTask
from django_celery_beat.schedulers import DatabaseScheduler, ModelEntry


class CustomModelEntry(ModelEntry):

    def __init__(self, model, app=None):
        """
        Admin에서 Task를 변경하면
        모든 Task를 가져와서 last_run_at을 초기화 시켜줘야
        Timezone 관계없이 Task가 수행될 수 있다.
        """
        model.last_run_at = None
        super().__init__(model, app)


class CustomDatabaseScheduler(DatabaseScheduler):
    Entry = CustomModelEntry
