from config.settings.base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


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

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
            "capacity": 1500,  # default 100
            "expiry": 10,  # default 60 seconds
        },
    },
}

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi_local.application"


"""
# CORS_ALLOW_CREDENTIALS=True 임에도 whitelist는 필요하다!
# CORS_ALLOW_ALL_ORIGINS = True <- 이거 있으면 whitelist 필요 x
CORS_ORIGIN_WHITELIST = [
    "https://localhost:8082",
    "http://localhost:8082",
    "https://localhost",
    "http://localhost",
]
"""

CORS_ALLOW_ALL_ORIGINS = (
    True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
)
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ["https://localhost", "https://192.168.1.243"]
