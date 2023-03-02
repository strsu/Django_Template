from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from config.exceptions.custom_exceptions import CustomParameterException


def calc():
    return 1 / 0


class BlogList(APIView):
    def get(self, request):
        if not ("date" in request.GET):
            raise CustomParameterException

        date = request.GET.get("date")

        calc()

        Value.objects.all()

        return Response(status=status.HTTP_200_OK)
