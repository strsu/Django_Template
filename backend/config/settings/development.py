from config.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": 5432,
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi_local.application"

# CORS_ALLOW_CREDENTIALS=True 임에도 whitelist는 필요하다!
CORS_ORIGIN_WHITELIST = ["https://localhost:8082", "http://localhost:8082"]
CORS_ALLOW_CREDENTIALS = True
