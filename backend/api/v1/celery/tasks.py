from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from config.celery import app

from django.conf import settings
from django.utils import timezone

from api.common.managers.async_fetch_manager import AsyncFetchManager
from api.v1.chat.service.socket_manager import SocketManager

from .base_task import BaseTask

import os
import time

import requests
import asyncio

"""
    코드가 변경되면 celery worker도 재시작 해줘야 된다.
"""


@shared_task
def sleep_task(*args, **kwargs):
    time.sleep(10)
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

    is_error_occured = False
    is_task_timeout = False
    is_revoke = False

    def do_something():
        """
        main ps에서 fork ps로 exception을 준다
        이때 이 함수에서 SoftTimeLimitExceeded에 따른 로직처리를 안해주면
        world 함수의 except에 걸리지 않기 때문에
        Task는 끝나지 않고 계속 돌아가는 문제가 발생한다.
        """

        url = "http://host.docker.internal/api/v1/soccer/level/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic YWRtaW46YWRtaW4=",
        }

        params = [{} for _ in range(10)]

        afm = AsyncFetchManager(headers)

        try:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(afm.get_data(url, params))
        except SoftTimeLimitExceeded as stle:
            raise SoftTimeLimitExceeded()
        except Exception as e:
            print(e)
        else:
            print(response)

    try:
        do_something()
    except SoftTimeLimitExceeded as stle:
        is_task_timeout = True
    except SystemExit:
        # 수동종료한 경우, flower에서 terminate 한 경우
        is_revoke = True
    except Exception as e:
        is_error_occured = True
    else:
        SocketManager.info("success")
    finally:
        if not is_revoke:
            print(f"finally - now_try_cnt: {now_try_cnt}, max_try_cnt : {max_try_cnt}")
            if is_task_timeout:
                SocketManager.info("fail")
                raise SoftTimeLimitExceeded()

            if is_error_occured:
                raise Exception()
