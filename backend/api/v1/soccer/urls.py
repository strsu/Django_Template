from django.urls import path
from api.v1.soccer import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.SoccerView.as_view(), name=""),
    path("<int:pk>/", views.SoccerView.as_view(), name=""),
    path("level/", views.SoccerLevelView.as_view(), name=""),
]
