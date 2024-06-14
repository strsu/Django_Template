from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async

from django.db import close_old_connections
from django.conf import settings

# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
import traceback


class JWTTokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        scope["user"] = None

        try:
            cookie_header = next(
                (value for key, value in scope["headers"] if key.lower() == b"cookie"),
                None,
            )

            if cookie_header is not None:
                cookies = dict(
                    cookie.split("=")
                    for cookie in cookie_header.decode("utf-8").split("; ")
                )
                cookies = {
                    key.lower(): value for key, value in cookies.items()
                }  # 헤더 키를 소문자로 변환

                x_authorization_value = cookies.get("x-authorization")
                token = cookies.get("token")

                if x_authorization_value is not None:
                    scope["user"] = await self.verify_jwt_token(x_authorization_value)
                elif token is not None:
                    scope["user"] = await self.verify_token(token)
                else:
                    print("Token header not found")
            else:
                print("Cookie header not found")

        except Exception as e:
            print(e)
            print(traceback.format_exc())

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def verify_jwt_token(self, token):
        from rest_framework_simplejwt.authentication import JWTAuthentication

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            return jwt_authentication.get_user(validated_token)
        except Exception as e:
            return None

    @database_sync_to_async
    def verify_token(self, token):
        from rest_framework.authtoken.models import Token

        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Exception as e:
            return None


def JWTAuthMiddlewareStack(app):
    return JWTTokenAuthMiddleware(app)
    # return JWTTokenAuthMiddleware(AuthMiddlewareStack(app))
