from django.urls import path, re_path
from api.v1.custom_permission import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.BlogApiView.as_view(), name=""),
]
