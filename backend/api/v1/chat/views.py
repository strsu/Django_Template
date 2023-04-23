from django.shortcuts import render, redirect
from config.settings.base import logger_info
import time

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ChatApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "chat/index.html", {})


class ChatPlayApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return redirect(f"/api/chat/")

    def post(self, request):
        room_name = request.data.get("room_name")
        user_name = request.data.get("user_name")
        return render(
            request,
            "chat/roomWithUser.html",
            {"room_name": room_name, "user_name": user_name},
        )


def index(request):
    # 여기서 request는 WSGIRequest 이다
    # 근데 위 drf의 request와 다른 객체이다!!!
    # 이건 장고 자체 rest 인 듯..!
    return render(request, "chat/index.html", {})
