from celery import shared_task
from config.celery import app

from django.conf import settings
from django.utils import timezone

from .base_task import BaseTask

import os
import time

"""
    코드가 변경되면 celery worker도 재시작 해줘야 된다.
"""

STATIC_ROOT = settings.STATIC_ROOT
MEDIA_ROOT = settings.MEDIA_ROOT


@shared_task
def sleep_task(sec=10):
    time.sleep(sec)
    return None


@app.task(
    max_retries=3, autoretry_for=(Exception,), default_retry_delay=10, queue="hipri"
)
def say_hello(*args, **kwargs):  # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    now_try_cnt = say_hello.request.retries
    max_try_cnt = say_hello.max_retries

    if now_try_cnt != max_try_cnt:
        ## NOTE - 오류가 일어나면 일단 작업은 수행하고, Celery Task는 실패로 기록한다!
        raise Exception()


@app.task(base=BaseTask, queue="hipri")
def world(*args, **kwargs):  # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    now_try_cnt = world.request.retries
    max_try_cnt = world.max_retries

    if now_try_cnt != max_try_cnt:
        raise Exception()
