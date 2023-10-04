from django.urls import path, re_path
from api.v1.aggregate import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("price/", views.PriceApiView.as_view(), name=""),
]
