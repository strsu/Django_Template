from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from api.v1.user import views

urlpatterns = [
    # 로그인 (JWT TOKEN)
    re_path(r"^token/$", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(r"^token/verify/$", views.MyTokenVerifyView.as_view(), name="token_verify"),
    re_path(r"^signin/$", views.SignViewSet.as_view({"post": "signin"}), name="signin"),
    re_path(r"^oauth/kakao/$", views.KakaoView.as_view(), name="kakao"),
    re_path(r"^oauth/kakao/callback/$", views.KakaoCallbackView.as_view(), name="kakao"),
    re_path(r"^oauth/google/$", views.GoogleView.as_view(), name=""),
    re_path(r"^oauth/google/callback/$", views.GoogleCallbackView.as_view(), name=""),
]
