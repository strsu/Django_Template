from django.urls import re_path

from api.v1.chat import consumer, androidConsumer

websocket_urlpatterns = [
    re_path(
        r"^ws/chat/(?P<room_name>[^/]+)/$", consumer.ChatConsumer.as_asgi()
    ),  # as_asgi()는 장고의 as_view()와 같은 역할을 한다
    re_path(
        r"^ws/mchat/(?P<room_name>[^/]+)/$", androidConsumer.AndroidConsumer.as_asgi()
    ),
]
