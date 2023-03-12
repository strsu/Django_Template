from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.exceptions.custom_exceptions import CustomParameterException
from blog.serializer import BlogSerializer

from datetime import datetime


class BlogList(APIView):
    # permission_classes = [IsAuthenticated] # 전역으로 설정되어 있어서 굳이 또 넣을 필요는 없다.
    # permission_classes = [AllowAny] # Auth가 전역으로 되어 있어서 해당 view에 Auth를 없애려면 이렇게 넣어주면 된다.
    authentication_classes = (JWTAuthentication, BasicAuthentication)

    def get(self, request):
        if not ("date" in request.GET):
            raise CustomParameterException

        date = request.GET.get("date")

        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        request.data에
            context, tags 있어야한다.
            date, user는 back에서 설정
        """
        if not ("content" in request.data):
            raise CustomParameterException

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            # user는 다음과 같이 설정할 수 있다.
            # serializer내 field에서 date를 지우고 여기서 넣어주면 된다!!
            serializer.save(user=request.user, date=datetime.now())
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=400)
