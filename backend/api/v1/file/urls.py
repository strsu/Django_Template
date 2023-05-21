from django.urls import path, re_path
from api.v1.file import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.FileView.as_view(), name=""),
    path("media/", views.VideoListView.as_view(), name=""),
]
