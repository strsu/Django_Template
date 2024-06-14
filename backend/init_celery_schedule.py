import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.settings"
)  # 장고 settings, manage.py 참조하면 된다.
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = (
    "true"  # 장고 3.0 이후 비동기 지원으로 인해 추가된 환경변수
)

import django
from django.utils import timezone

django.setup()  # 장고 프로젝트 셋업

from django_celery_beat.models import PeriodicTask, PeriodicTasks

PeriodicTask.objects.update(last_run_at=None)
PeriodicTasks.changed()
