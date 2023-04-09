from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from config.exceptions.custom_exceptions import CustomParameterException

from api.v1.file.models import File
from api.v1.file.serializer import FileSerializer

from datetime import datetime


class FileView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        file = File.objects.get(code=request.GET.get("code"))
        file_path = f"/opt/staticfiles/chat/img/{file.path}"
        with open(file_path, "rb") as f:
            file_data = f.read()

        # HttpResponse로 파일 응답
        response = HttpResponse(file_data, content_type="text/plain")
        response["Content-Disposition"] = f'attachment; filename="{file.name}"'
        return response
