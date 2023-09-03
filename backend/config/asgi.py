"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack  # 추가
from channels.routing import ProtocolTypeRouter, URLRouter  # URLRouter 추가
from channels.security.websocket import AllowedHostsOriginValidator

from api.v1.chat import routing  # chat import
from config.middleware.TokenAuthMiddleware import JWTAuthMiddlewareStack

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
        ),
    }
)
