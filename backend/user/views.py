from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializer import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
