from django.urls import path, re_path
from api.v1.celery_practice import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.CeleryPacticeView.as_view(), name=""),
]
