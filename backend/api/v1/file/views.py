from django.shortcuts import render

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
    ...
