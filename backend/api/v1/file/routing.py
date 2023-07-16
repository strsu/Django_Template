from django.urls import re_path, path

from api.v1.file import consumer

websocket_urlpatterns = [
    re_path(
        r"^ws/chat/$", consumer.Consumer.as_asgi()
    ),  # as_asgi()는 장고의 as_view()와 같은 역할을 한다
]
