from django.urls import path

from api.v1.chat import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("<str:room_name>/<str:user_name>/", views.roomWithUser, name="roomWithUser"),
]
