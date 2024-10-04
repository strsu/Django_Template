from django.urls import path
from api.v1.slack import views

urlpatterns = [
    path("", views.SlackInteractiveView.as_view(), name=""),
    path("command/", views.SlackCommandView.as_view(), name=""),
    path("verify/", views.SlackUserVerifyView.as_view(), name="verify"),
]
