from django.urls import path

from api.v1.chat import views

urlpatterns = [
    path("", views.ChatApiView.as_view(), name="index"),
    path("play/", views.ChatPlayApiView.as_view(), name="play"),
]
