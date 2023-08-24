from django.urls import path, re_path
from api.v1.serializer_without_model import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("<str:type>/", views.IntegrationApiView.as_view(), name=""),
]
