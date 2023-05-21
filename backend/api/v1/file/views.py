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
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


class VideoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        video_dict = {}

        def get_video_list(path):
            nonlocal video_dict

            res = requests.get(
                f"https://nginx/listing/media{path}",
                headers={"Content-Type": "application/json"},
                verify=False,
            )

            if res.status_code == 200:
                file_list = res.json()
                if file_list:
                    for file in file_list:
                        if file["name"] == "$RECYCLE.BIN":
                            continue
                        if file["type"] == "directory":
                            get_video_list(f"{path}{file['name']}")
                        else:
                            if ".mp4" in file["name"]:
                                if path[1:] not in video_dict:
                                    video_dict[path[1:]] = []

                                video_dict[path[1:]].append(file["name"])

        get_video_list("/")

        return Response(video_dict, status=200)
