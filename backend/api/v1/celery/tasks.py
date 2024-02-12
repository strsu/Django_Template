from celery import shared_task
from config.celery import app

from django.conf import settings
from django.utils import timezone

import os
import time

"""
    코드가 변경되면 celery worker도 재시작 해줘야 된다.
"""

STATIC_ROOT = settings.STATIC_ROOT
MEDIA_ROOT = settings.MEDIA_ROOT


@shared_task
def file_task(filename):

    format = "%Y-%m-%d %H:%M:%S"

    filename += str(timezone.now().strftime(format))
    time.sleep(60)
    f = open(os.path.join(STATIC_ROOT, f"DD_{filename}.log"), "w", encoding="utf-8")
    f.write("testss")
    f.close()

    return None


@app.task
def say_hello(*args, **kwargs):  # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    print("Hello, celery!")
