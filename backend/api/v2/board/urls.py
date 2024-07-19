from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.BoardView.as_view(),
        name="",
    ),
]
