from django.utils import timezone
from django_celery_beat.schedulers import DatabaseScheduler, ModelEntry

from kombu.utils.json import dumps, loads


class CustomModelEntry(ModelEntry):

    def __init__(self, model, app=None):
        """
        * model.last_run_at = None
            Admin에서 Task를 변경하면
            모든 Task를 가져와서 last_run_at을 초기화 시켜줘야
            Timezone 관계없이 Task가 수행될 수 있다.
        * kwargs - https://www.notion.so/youngjae-park/Queue-11dd352a8ffe80aeb0a7c6c3bc06f38a?pvs=4
            Beat가 스케줄로 등록된 Task를 Queue에 넣을 때 넣는 시간을 넣기위한 작업
            이렇게 해야 Task가 작업을 수행할 때 정확히 해당작업이 언제를 기준으로 작업을 처리해야 하는지 알 수 있다.
        """
        kwargs = loads(model.kwargs or "{}")
        if kwargs.get("executed_at") is None:
            kwargs["executed_at"] = timezone.now()
            model.kwargs = dumps(kwargs)

        model.last_run_at = None

        super().__init__(model, app)


class CustomDatabaseScheduler(DatabaseScheduler):
    Entry = CustomModelEntry
