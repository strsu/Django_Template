from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload
from django.conf import settings

import os
import sys
import time
import shlex
import subprocess

from django_celery_beat.models import PeriodicTask


def init_celery():
    PeriodicTask.objects.update(last_run_at=None)


def start_celery(action):

    init_celery()

    print("Stoping lopri Worker")
    cmd = f"celery multi stopwait lopri -E -A config --pidfile={settings.BASE_DIR}/lopri.pid"
    subprocess.call(shlex.split(cmd))

    print("Starting lopri Worker")
    cmd = f"celery multi start lopri -E -A config -Q lopri -P prefork -l info --pidfile={settings.BASE_DIR}/lopri.pid --logfile={settings.BASE_DIR}/log/lopri.log"
    subprocess.call(shlex.split(cmd))

    print("Stoping hipri Worker")
    cmd = f"celery multi stopwait hipri -E -A config --pidfile={settings.BASE_DIR}/hipri.pid"
    subprocess.call(shlex.split(cmd))

    print("Starting hipri Worker")
    cmd = f"celery multi start hipri -E -A config -Q hipri -P prefork -l info --pidfile={settings.BASE_DIR}/hipri.pid --logfile={settings.BASE_DIR}/log/hipri.log"
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
