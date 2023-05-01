from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenVerifySerializer,
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 토큰에 추가로 주고 싶은 필드 넣기
        token["name"] = user.username

        return token


class MyTokenVerifySerializer(TokenVerifySerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 토큰에 추가로 주고 싶은 필드 넣기
        token["name"] = user.username
        # ...

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
