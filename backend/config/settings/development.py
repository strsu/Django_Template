from config.settings.base import *

DEBUG = True

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

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS = ["https://localhost", "https://192.168.1.243"]
