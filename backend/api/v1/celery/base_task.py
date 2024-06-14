from celery import Task
import logging

debug_logger = logging.getLogger("debug")


class BaseTask(Task):
    """
    @app.task(base=BaseTask)
    def add(x, y):
        raise KeyError()
    """

    autoretry_for = (Exception,)
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
        pass
