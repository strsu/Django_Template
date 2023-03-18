from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from api.v1.user.serializer import MyTokenObtainPairSerializer, MyTokenVerifySerializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class MyTokenVerifyView(TokenVerifyView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenVerifySerializer
