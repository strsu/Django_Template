from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload
from django.conf import settings

import os
import shlex
import subprocess

from django_celery_beat.models import PeriodicTask

WORKER = os.path.join(settings.BASE_DIR, "celery.pid")


def init_celery():
    try:
        os.remove(WORKER)
    except Exception as e:
        print(e)

    PeriodicTask.objects.update(last_run_at=None)


def start_celery(action):
    init_celery()

    cmd = 'pkill -f "celery worker"'
    subprocess.call(shlex.split(cmd))
    cmd = f"celery -A config worker --pool prefork --loglevel=info --pidfile={WORKER}"
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):

    def add_arguments(self, parser):
        ## 명령 추가 인자를 받는 방법
        parser.add_argument("action", type=str)

    def handle(self, *args, **options):
        action = options["action"]

        autoreload.run_with_reloader(start_celery, action=action)


# commands: python3 command.py celery_worker start
# commands: python3 command.py celery_worker restart
