from django.urls import path

from api.v1.carrot import views

urlpatterns = [
    path("rooms/", views.ChatRoomListView.as_view(), name=""),
    path(
        "rooms/<int:pk>/conversation/",
        views.ChatConversationListView.as_view(),
        name="",
    ),
]
