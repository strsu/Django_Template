from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.user.models import User
from api.v1.user.serializer import MyTokenObtainPairSerializer, MyTokenVerifySerializer

from config.exceptions.custom_exceptions import CustomException
from api.common.message import UserFault


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class MyTokenVerifyView(TokenVerifyView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenVerifySerializer


class SignViewSet(ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = User.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    def signin(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
        except Exception as e:
            raise CustomException(UserFault.PARAMETER_ERROR)

        try:
            user = self.get_queryset().get(email=email)
        except User.DoesNotExist:
            raise CustomException(UserFault.NOT_FOUND)
        else:
            is_login = user.check_password(password)
            if not is_login:
                raise CustomException(UserFault.USRE_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(status=200)
