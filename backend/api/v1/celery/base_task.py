from celery import Task
from celery.exceptions import SoftTimeLimitExceeded

from django.db import close_old_connections

import logging

debug_logger = logging.getLogger("debug")


class BaseTask(Task):
    """
    @app.task(base=BaseTask)
    def add(x, y):
        raise KeyError()
    """

    autoretry_for = (Exception,)  # 모든 Exception에 대해 retry
    dont_autoretry_for = (
        SoftTimeLimitExceeded,
    )  # SoftTimeLimitException은 retry 안 함
    max_retries = 3  # 3회 재시도
    default_retry_delay = 10  # 10초 후 재시도
    soft_time_limit = 60 * 15  # 15분

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        TASK 최종 실패 후 호출
        * exc : exception 종류
        """
        debug_logger.info(f"최종실패 : {self.name} - {task_id}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        debug_logger.info(f"{self.request.retries}회 재시도 : {self.name} - {task_id}")

    def on_success(self, retval, task_id, args, kwargs):
        """
        TASK 성공 후 호출
        """
        debug_logger.info(f"최종성공 : {self.name} - {task_id}")

    def before_start(self, task_id, args, kwargs):
        """
        TASK 시작 전 실행된다.
        """
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        on_failure, on_auccess 함수 이후에 호출
         -> FAILURE / SUCCESS 후에 실행된다.
        """
        """
        django-db-geventpool 을 사용하면 close_old_connections() 를 꼭 호출해야 한다.

        If you are using django with celery (or other), or have code that manually spawn greenlets it will not be sufficient to set CONN_MAX_AGE to 0. 
        Django only checks for long-live connections when finishing a request - 
        So if you manually spawn a greenlet (or task spawning one) its connections will not get cleaned up and will live until timeout. 
        In production this can cause quite some open connections and while developing it can hamper your tests cases.

        To solve it make sure that each greenlet function (or task) either sends 
        the django.core.signals.request_finished signal or calls django.db.close_old_connections() right before it ends
        """
        close_old_connections()
        pass
