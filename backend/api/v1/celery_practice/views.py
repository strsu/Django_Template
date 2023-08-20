from django.shortcuts import render

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.v1.celery_practice.tasks import file_task


class CeleryPacticeView(APIView):
    # permission_classes = [IsAuthenticated] # 전역으로 설정되어 있어서 굳이 또 넣을 필요는 없다.
    # permission_classes = [AllowAny] # Auth가 전역으로 되어 있어서 해당 view에 Auth를 없애려면 이렇게 넣어주면 된다.
    authentication_classes = (JWTAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_id="시스템설정 옵션 조희",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="api/v1/celery_practice/",
                required=True,
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            "200": openapi.Response(
                description="요청 성공",
                examples={
                    "application/json": {
                        "results": {
                            "generation_hour": "05-21",
                        }
                    },
                },
            ),
            "400": openapi.Response(
                description="잘못된 요청",
                examples={"application/json": {"message": "요청 실패"}},
            ),
        },
    )
    def get(self, request):
        file_task.delay("test")
        return Response(status=status.HTTP_200_OK)
