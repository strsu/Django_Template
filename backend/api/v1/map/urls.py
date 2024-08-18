from django.urls import path, re_path
from api.v1.orm import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("map/", views.PriceApiView.as_view(), name=""),
]
