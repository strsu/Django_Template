from typing import List, Tuple
from datetime import timedelta
from pathlib import Path

import requests
import socket
import logging
import re
import os


WHOAMI = os.getenv("WHOAMI")
if WHOAMI:
    WHOAMI = WHOAMI.lower()
else:
    print("Need to setting WHOAMI variable")
    exit()

if WHOAMI not in ("local", "dev", "prod"):
    print("WHOAMI must be one of local, dev, prod")
    exit()

MY_PUBLIC_IP = "localhost"
MY_LOCAL_IP = socket.gethostbyname(socket.gethostname())
HOST = os.getenv("HOST").split(",")

if WHOAMI in ("prod", "dev"):
    # 한국에서만 사용가능
    try:
        req = requests.get("http://ipconfig.kr", timeout=10)
        MY_PUBLIC_IP = re.search(
            r"IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", req.text
        )[1]
    except Exception as e:
        print("##", e)

    if MY_PUBLIC_IP == "localhost":
        # 해외에서 사용가능
        try:
            MY_PUBLIC_IP = requests.get(
                "https://api.ipify.org", timeout=10
            ).content.decode("utf8")
        except Exception as e:
            print("##", e)

## --- Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)


MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

# --- sass
SASS_OUTPUT_STYLE = "compact"
SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, STATIC_URL)

ROOT_URLCONF = "config.urls"
APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

# MEDIA CONFIGURATION
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024 * 5  # 업로드 파일 사이즈 1gb * 5

# -- AWS Setting
if WHOAMI == "prod":
    AWS_REGION = "asia"  # AWS서버의 지역
    AWS_STORAGE_BUCKET_NAME = "django"  # 생성한 버킷 이름
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # 버킷이름.s3.AWS서버지역.amazonaws.com 형식
    # AWS_S3_ENDPOINT_URL = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
    AWS_S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT")

    # Static Setting
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # Media Setting
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/"

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    SASS_PROCESSOR_ROOT = STATIC_URL

# --- Locale settingss
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"

USE_I18N = True
USE_TZ = False

# --- Security
SECRET_KEY = os.getenv("SECRET_KEY")
SESSION_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = "DENY"  # Prevent iframes. Can be overwritten per view using the @xframe_options_.. decorators


# --- variable
BROKER_URL = os.getenv("BROKER_URL_")
BROKER_PORT = os.getenv("BROKER_PORT_")
BROKER_PASSWORD = os.getenv("REDIS_PASSWORD")

# --- crontab
envs = []
for envkey in os.environ.keys():
    envs.append(envkey + "=" + os.environ[envkey])
CRONTAB_COMMAND_PREFIX = " ".join(envs)
CRONTAB_DJANGO_SETTINGS_MODULE = "config.settings.base"
# CRONJOBS = [
#     (
#         "*/1 * * * *",
#         "cron.test.ttt",
#         ">> " + os.path.join(BASE_DIR, "log/cron.log") + " 2>&1 ",
#     ),
# ]


# Application definition

DJANGO_APPS = [
    "daphne",  # 이걸 넣으면 runserver를 asgi로 올릴 수 있다.
    "admin_tools",
    "admin_tools.theming",
    "admin_tools.menu",
    "admin_tools.dashboard",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "django_celery_beat",
]

THIRD_APPS = [
    "channels",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "sass_processor",
    "corsheaders",  # CORS 관련 추가
    "django_elasticsearch_dsl",
    "django_filters",  # django-filter 등록
    "django_crontab",
    "storages",
    "graphene_django",
]

if WHOAMI != "prod":  # 운영이 아닌 경우에만!
    THIRD_APPS.append(
        "debug_toolbar"
    )  # 이걸 너무 빨리 import하면 제대로 동작하지 않는다!!!

LOCAL_APPS = [
    "config.admin_page",
    "api.common",
    "api.v1.chat",
    "api.v1.file",
    "api.v1.blog",
    "api.v1.user",
    "api.v1.soccer",
    "api.v1.rating",
    "api.v1.history",
    "api.v1.celery",
    "api.v1.model_view_set",
    "api.v1.serializer_without_model",
    "api.v1.orm",
    "api.v1.map",
    "api.v1.carrot",
    "api.v1.board",
    "api.v2.board",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS 관련 추가
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.LoggingMiddleware.LoggingMiddleware",  # Custom Middleware
]

if WHOAMI != "prod":  # 운영이 아닌 경우에만!
    MIDDLEWARE.insert(
        3, "debug_toolbar.middleware.DebugToolbarMiddleware"
    )  # 맨 앞에 넣으면 인식 안됨

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        # "APP_DIRS": True,  # loaders를 추가했더니 APP_DIRS가 False 여야 장고가 켜진다. app_dirs must not be set when loaders is defined
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "admin_tools.template_loaders.Loader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

SECURE_SCHEMES = ["http", "https"]
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        # 모든 view에 Auth 체크가 적용된다.
        # "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",  # Get 은 호출 되도록 - 단점이 생김, UserFilter가 반드시 필요한 곳은 IsAuthenticated 설정을 따로 해줘야 한다.
    ),
    # test코드 돌릴 때
    # self.client.force_login(self.owner) 을 사용하려면 SessionAuthentication이 반드시 필요하다!
    # self.client.force_authenticate(user=self.test) 이거는 SessionAuthentication 없어도 동작!
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",  # airflow 등 변하지 않는 토큰이 필요한 곳에 필요.
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        # "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",  # UserRate와 같이 동작해서, 같이 선언하면 안된다.
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/day",
        "user": "2000/minute",
        "board": "5/day",
        "premium_user": "2000/minute",
        "light_user": "5/day",
    },
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "config.exceptions.api_exception.custom_exception_handler",
    # "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 50,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Django Template",
    "DESCRIPTION": "장고연습장",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "user.User"  # 커스텀 유저 모델 사용, "어플리케이션명.모델명"

# simple jwt 옵션 제공
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),  # timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "uuid",  # jwt에 USER_ID_FIELD의 Key값 -> email: <user email>
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.MyTokenObtainPairSerializer",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CELERY SETTINGS
CELERY_ENABLE_UTC = False
CELERY_ALWAYS_EAGER = False
CELERY_TIMEZONE = "Asia/Seoul"

"""
env에 BROKER_URL 변수가 있으면, celery worker에서 os의 env에서 broker_url을 가져온다
즉, settings의 broker_url을 사용하지 않음
따라서 env파일에 broker_url을 넣을 때 이름을 broker_url_ 등 조금 변형해서 사용해야 한다.
"""

CELERY_BROKER_URL = f"redis://:{BROKER_PASSWORD}@{BROKER_URL}:{BROKER_PORT}"
CELERY_BROKER_TRANSPORT = "redis"  # 이걸 넣으니까 rabbitmq가 아니라 redis에 연결한다.
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_retries": 5,
    "interval_start": 0,  # 첫 번째 재시도를 즉시 수행
    "interval_step": 0.2,  # 이후 각 재시도 간격을 200ms씩 증가
    "interval_max": 0.5,  # 재시도 간격이 0.5초를 넘지 않도록 설정
}

# CELERY_RESULT_BACKEND = f"redis://:{BROKER_PASSWORD}@{BROKER_URL}:{BROKER_PORT}"
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# CELERY_WORKER_STATE_DB = True
CELERY_RESULT_PERSISTENT = True

CELERY_ACKS_LATE = True
CELERY_PREFETCH_MULTIPLIER = 1
"""
[x] PREFETCH_MULTIPLIER
How many messages to prefetch at a time multiplied by the number of concurrent processes. 
The default is 4 (four messages for each process). The default setting is usually a good choice, 
however - if you have very long running tasks waiting in the queue and you have to start the workers, 
note that the first worker to start will receive four times the number of messages initially. 
Thus the tasks may not be fairly distributed to the workers.

To disable prefetching, set worker_prefetch_multiplier to 1. 
Changing that setting to 0 will allow the worker to keep consuming as many messages as it wants.
"""

# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULER = (
    "config.schedulers:CustomDatabaseScheduler"  # custom 스케줄러 적용
)

# Elastic
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": f"{os.getenv('ELASTICSEARCH_DSL_IP')}:{os.getenv('ELASTICSEARCH_DSL_PORT')}"
    }
}

# --- Databse
DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql_psycopg2",
        # "ENGINE": "django.contrib.gis.db.backends.postgis",
        # "ENGINE": "dj_db_conn_pool.backends.postgresql", # postgis 사용 불가
        "ENGINE": "django_db_geventpool.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "OPTIONS": {"MAX_CONNS": 20, "REUSE_CONNS": 10},  # For 'django_db_geventpool'
    }
}

# --- Graphql, Cache
"""
내장 core.cache
    -> 이걸 사용하면 cache를 통한 race condition -> SETNX 기능을 사용할 수 없다.
그래서 django-redis를 사용해야 한다.
"""
CACHES = {
    # "default": {
    #     "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #     "LOCATION": [f"redis://:{BROKER_PASSWORD}@{BROKER_URL}:{BROKER_PORT}"],
    # },
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{BROKER_PASSWORD}@{BROKER_URL}:{BROKER_PORT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
CACHE_TTL = 60 * 1500  # 60초 * 1500분 = 25시간

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [
                f"redis://:{BROKER_PASSWORD}@{BROKER_URL}:{BROKER_PORT}"  # RedisPubSubChannelLayer
            ],
            "capacity": 1500,  # default 100, Once a channel is at capacity, it will refuse more messages.
            "expiry": 10,  # default 60 seconds
        },
    },
    # "default": {
    #     "BACKEND": "channels_redis.core.RedisChannelLayer",
    #     "CONFIG": {
    #         "hosts": [
    #             (f"{BROKER_PASSWORD}@{BROKER_URL}", BROKER_PORT)
    #         ],  # RedisChannelLayer
    #         "capacity": 1500,  # default 100, Once a channel is at capacity, it will refuse more messages.
    #         "expiry": 10,  # default 60 seconds
    #     },
    # },
}

ASGI_THREADS = 1000

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# logging
logger_error = logging.getLogger("logstash_error")
logger_info = logging.getLogger("logstash_info")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "simple": {"format": "%(message)s"},
        "loki": {"format": "%(message)s"},
        "debug": {
            "format": "%(asctime)s pid:%(process)s {%(pathname)s:%(lineno)d} - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "query": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log/response.log"),
            "when": "D",  # when: 시간 단위 ('S' - 초, 'M' - 분, 'H' - 시간, 'D' - 일, 'W' - 주차, 'midnight' - 자정)
            "interval": 1,  # interval: 로그 파일을 회전시키는 시간 간격
            "backupCount": 30,  # 보존할 백업 파일 수
            "formatter": "loki",
        },
        "exception": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log/exception.log"),
            "when": "D",  # when: 시간 단위 ('S' - 초, 'M' - 분, 'H' - 시간, 'D' - 일, 'W' - 주차, 'midnight' - 자정)
            "interval": 1,  # interval: 로그 파일을 회전시키는 시간 간격
            "backupCount": 30,  # 보존할 백업 파일 수
            "formatter": "standard",
        },
        "django.server": {
            # python manage.py runserver로 작동하는 개발 서버에서만 사용하는 핸들러로 콘솔에 로그를 출력한다.
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            # 로그 내용을 이메일로 전송하는 핸들러로, 로그 레벨이 ERROR 이상이고 DEBUG=False 일때만 로그를 전송한다.
            # 이 핸들러를 사용하려면 환경설정 파일에 ADMINS라는 항목을 추가하고 관리자 이메일을 등록해야 한다
            # (예: ADMINS = ['pahkey@gmail.com']). 그리고 이메일 발송을 위한 SMTP 설정도 필요하다.
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "debug": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log/debug.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
            "formatter": "debug",
        },
        "logstash_info": {
            "level": "INFO",
            "class": "logstash.TCPLogstashHandler",
            "host": os.getenv("ELASTICSEARCH_DSL_IP"),
            "port": os.getenv("LOGSTASH_PORT"),  # Default value: 5959
            "version": 1,
            "message_type": "django_info",
            "tags": ["django", "dev"],
        },
        "logstash_error": {
            "level": "ERROR",
            "class": "logstash.TCPLogstashHandler",
            "host": os.getenv("ELASTICSEARCH_DSL_IP"),
            "port": os.getenv("LOGSTASH_PORT"),  # Default value: 5959
            "version": 1,
            "message_type": "django_error",
            "tags": ["django", "dev"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": ["query"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "middleware": {
            "handlers": ["file"],
            "level": "INFO",
        },
        "exception": {
            "handlers": ["exception"],
            "level": "ERROR",
        },
        "debug": {
            "handlers": ["debug"],
            "level": "DEBUG",
        },
        "logstash_info": {
            # "handlers": ["console", "mail_admins", "file"],
            # 위 처럼 handler가 여러개면 중복으로 로그가 쌓인다
            # 때문에 분리가 필요!!
            "handlers": ["logstash_info"],
            "level": "INFO",
        },
        "logstash_error": {
            # "handlers": ["console", "mail_admins", "file"],
            "handlers": ["logstash_error"],
            "level": "ERROR",
        },
    },
}
