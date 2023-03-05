from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from config.exceptions.custom_exceptions import CustomParameterException


def calc():
    return 1 / 0


class BlogList(APIView):
    # permission_classes = [IsAuthenticated] # 전역으로 설정되어 있어서 굳이 또 넣을 필요는 없다.
    # permission_classes = [AllowAny] # Auth가 전역으로 되어 있어서 해당 view에 Auth를 없애려면 이렇게 넣어주면 된다.

    def get(self, request):
        if not ("date" in request.GET):
            raise CustomParameterException

        date = request.GET.get("date")

        calc()

        Value.objects.all()

        return Response(status=status.HTTP_200_OK)
