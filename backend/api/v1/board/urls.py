from rest_framework import routers
from django.urls import path

from api.v1.board import views


router = routers.SimpleRouter(trailing_slash=True)
router.register(r"", views.BoardView)
router.register(r"(?P<b_id>\d+)/comment", views.BoardCommentdView)


urlpatterns = [
    path(
        "<int:b_id>/comment/<int:c_id>/like/",
        views.BoardCommentLikeView.as_view(),
        name="",
    ),
    path("<int:b_id>/like/", views.BoardLikeView.as_view(), name=""),
    path("<int:b_id>/image/", views.BoardImageView.as_view(), name=""),
] + router.urls
