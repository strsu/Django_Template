from django.urls import path
from api.v1.rating import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.MovieView.as_view(), name=""),
    path("<int:pk>/", views.MovieView.as_view(), name=""),
]
