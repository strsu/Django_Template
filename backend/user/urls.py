from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from user.views import MyTokenObtainPairView

urlpatterns = [
    # 로그인 (JWT TOKEN)
    re_path("token", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    re_path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
