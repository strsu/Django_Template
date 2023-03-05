from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from user.views import MyTokenObtainPairView, MyTokenVerifyView

urlpatterns = [
    # 로그인 (JWT TOKEN)
    re_path(r"^token/$", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(r"^token/verify/$", TokenVerifyView.as_view(), name="token_verify"),
]
