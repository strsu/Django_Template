from django.urls import path, re_path
from api.v1.map import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("cloth/", views.ClothingCollectingBoxView.as_view(), name=""),
]
