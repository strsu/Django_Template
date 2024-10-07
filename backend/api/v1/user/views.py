from django.shortcuts import render, redirect

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model
from api.v1.user.serializer import MyTokenObtainPairSerializer, MyTokenVerifySerializer

from config.exceptions.custom_exceptions import CustomException
from api.common.message import UserFault

import requests


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class MyTokenVerifyView(TokenVerifyView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenVerifySerializer


class SignViewSet(ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = get_user_model().objects.all()
    serializer_class = None

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
        except get_user_model().DoesNotExist:
            raise CustomException(UserFault.NOT_FOUND)
        else:
            is_login = user.check_password(password)
            if not is_login:
                raise CustomException(UserFault.USRE_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(status=200)


class KakaoCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")

        if code:
            ## Access Token 받아오기
            data = {
                "grant_type": "authorization_code",
                "client_id": "af4d2b8e69b31a39c9645bbd6be0cd69",
                "redirect_uri": "https://localhost/api/v1/user/oauth/kakao/callback/",
                "code": code,
                "client_secret": "aSGcHRePSGuyYRfwzaQ0gwQLD6Awm7dW",
            }

            kakao_token_api = "https://kauth.kakao.com/oauth/token"

            response = requests.post(kakao_token_api, data=data)
            if response.status_code != 200:
                print(response.text)
                return Response(status=500)

            result = response.json()
            access_token = result.get("access_token")

            ## 사용자 정보 받아오기
            kakao_user_info_api = "https://kapi.kakao.com/v2/user/me"
            header = {
                "Authorization": f"Bearer {access_token}",
            }

            response = requests.post(kakao_user_info_api, headers=header)
            if response.status_code != 200:
                print(response.text)
                return Response(status=500)

            result = response.json()
            print(result)
            user_id = result.get("id")

            if user_id:
                # 유저찾기 및 생성
                try:
                    user = get_user_model().objects.get(email=user_id)
                except Exception as e:
                    user = get_user_model().objects.create(email=user_id)
                finally:
                    # 이후 인증은 자체 토큰으로 진행한다
                    refresh = RefreshToken.for_user(user)
                    response = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }

                    return Response(response, status=200)

        return Response(status=400)


class KakaoView(APIView):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize"
        redirect_url = "https://localhost/api/v1/user/oauth/kakao/callback/"
        client_id = "af4d2b8e69b31a39c9645bbd6be0cd69"

        url = f"{kakao_api}?response_type=code&client_id={client_id}&redirect_uri={redirect_url}"

        return redirect(url)
