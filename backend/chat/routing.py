from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(
        r"^ws/chat/(?P<room_name>[^/]+)/$", consumer.ChatConsumer.as_asgi()
    ),  # as_asgi()는 장고의 as_view()와 같은 역할을 한다
]
