import multiprocessing
import logging
from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthCheckFilter())


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "HealthChecker" not in record.getMessage()


# workers = multiprocessing.cpu_count() * 2
workers = 1
worker_class = "gevent"
thread = 4

bind = "0.0.0.0:8000"
timeout = 0

errorlog = "log/error.log"

# django setting.py에서 'disable_existing_loggers': False 로 해야 한다고 함
loglevel = "info"
accesslog = "log/access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
logger_class = CustomGunicornLogger


# daemon = True
capture_output = True

spew = False  # True명 모든 내용을 console에 출력한다. 배포는 False로
reload = True
