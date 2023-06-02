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

CORS_ORIGIN_WHITELIST = ["https://localhost", "http://localhost"]
CORS_ALLOW_CREDENTIALS = False

CSRF_TRUSTED_ORIGINS = ["http://*", "https://*"]
