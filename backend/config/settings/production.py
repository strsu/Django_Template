from config.settings.base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": POSTGRES["POSTGRES_DB"],
        "USER": POSTGRES["POSTGRES_USER"],
        "PASSWORD": POSTGRES["POSTGRES_PASSWORD"],
        "HOST": POSTGRES["POSTGRES_HOST"],
        "PORT": POSTGRES["POSTGRES_PORT"],
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

CORS_ORIGIN_WHITELIST = [
    "http://anhae.site",
    "https://anhae.site",
    "http://localhost",
    "https://localhost",
    "https://172.104.96.127",
]
CSRF_TRUSTED_ORIGINS = [
    "http://anhae.site",
    "https://anhae.site",
    "http://localhost",
    "https://localhost",
    "https://172.104.96.127",
]
