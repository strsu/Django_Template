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

if WHOAMI in ("prod", "dev"):
    try:
        req = requests.get("http://ipconfig.kr")
        MY_PUBLIC_IP = re.search(
            r"IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", req.text
        )[1]
    except Exception as e:
        print("##", e)

## --- Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)

SASS_OUTPUT_STYLE = "compact"
SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, STATIC_URL)

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

ROOT_URLCONF = "config.urls"
APPEND_SLASH = True

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
    "debug_toolbar",
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
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "channels",
    "drf_yasg",
    "sass_processor",
    "corsheaders",  # CORS 관련 추가
    "django_elasticsearch_dsl",
    "django_filters",  # django-filter 등록
    "django_crontab",
]

LOCAL_APPS = [
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
    "api.v1.board",
    "api.v1.orm",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS 관련 추가
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.LoggingMiddleware.LoggingMiddleware",  # Custom Middleware
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        # "APP_DIRS": True, # loaders를 추가했더니 APP_DIRS가 False 여야 장고가 켜진다.
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
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
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
        "anon": "100/day",
        "user": "10/day",
        "board": "5/day",
        "premium_user": "50/minute",
        "light_user": "5/day",
    },
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "config.exceptions.api_exception.custom_exception_handler",
    # "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
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
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "email",  # jwt에 USER_ID_FIELD의 Key값 -> email: <user email>
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

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

# MEDIA CONFIGURATION
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024 * 5  # 업로드 파일 사이즈 1gb * 5

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CELERY SETTINGS
CELERY_ENABLE_UTC = False
CELERY_ALWAYS_EAGER = False
CELERY_TIMEZONE = "Asia/Seoul"

CELERY_BROKER_URL = f"redis://{os.getenv('BROKER_URL')}:{os.getenv('BROKER_PORT')}"
CELERY_BROKER_TRANSPORT = "redis"  # 이걸 넣으니까 rabbitmq가 아니라 redis에 연결한다.
# CELERY_RESULT_BACKEND = f"redis://{os.getenv('BROKER_URL')}:{os.getenv('BROKER_PORT')}"
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

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Elastic
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": f"{os.getenv('ELASTICSEARCH_DSL_IP')}:{os.getenv('ELASTICSEARCH_DSL_PORT')}"
    }
}

# --- Databse, Cache
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

CACHE_TTL = 60 * 1500  # 60초 * 1500분 = 25시간
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [f"redis://{os.getenv('BROKER_URL')}:{os.getenv('BROKER_PORT')}"],
    }
}

CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            # "hosts": [(os.getenv('BROKER_URL'), os.getenv('BROKER_PORT'))], # RedisChannelLayer
            "hosts": [
                f"redis://{os.getenv('BROKER_URL')}:{os.getenv('BROKER_PORT')}"  # RedisPubSubChannelLayer
            ],
            "capacity": 1500,  # default 100, Once a channel is at capacity, it will refuse more messages.
            "expiry": 10,  # default 60 seconds
        },
    },
}

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
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
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
