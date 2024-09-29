from django.urls import re_path, path

from api.v1.chat import consumer, consumer_android, consumer_user
from api.v1.carrot import consumer as corrot

websocket_urlpatterns = [
    re_path(
        r"^ws/chat/(?P<room_name>[^/]+)/$", consumer.ChatConsumer.as_asgi()
    ),  # as_asgi()는 장고의 as_view()와 같은 역할을 한다
    re_path(r"^ws/goods/$", corrot.ChatConsumer.as_asgi()),
    path(
        "ws/chat/<str:room_name>/<str:user_name>/",
        consumer_user.ChatConsumer.as_asgi(),
    ),  # as_asgi()는 장고의 as_view()와 같은 역할을 한다
    re_path(
        r"^ws/mchat/(?P<room_name>[^/]+)/$", consumer_android.AndroidConsumer.as_asgi()
    ),
]
