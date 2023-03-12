from django.shortcuts import render

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.exceptions.custom_exceptions import CustomParameterException

from blog.models import Blog
from blog.serializer import BlogSerializer

from datetime import datetime


class BlogApiView(APIView):
    # permission_classes = [IsAuthenticated] # 전역으로 설정되어 있어서 굳이 또 넣을 필요는 없다.
    # permission_classes = [AllowAny] # Auth가 전역으로 되어 있어서 해당 view에 Auth를 없애려면 이렇게 넣어주면 된다.
    authentication_classes = (JWTAuthentication, BasicAuthentication)

    def get(self, request):
        if not ("id" in request.GET):
            raise CustomParameterException

        id = request.GET.get("id")
        data = Blog.objects.get(id=id)
        serializer = BlogSerializer(instance=data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        request.data에
            context, tags 있어야한다.
            date, user는 back에서 설정
        """
        if not ("content" in request.data):
            raise CustomParameterException

        deserializer = BlogSerializer(data=request.data)
        if deserializer.is_valid():
            # user는 다음과 같이 설정할 수 있다.
            # serializer내 field에서 date를 지우고 여기서 넣어주면 된다!!
            deserializer.save(user=request.user, date=datetime.now())
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=400)


class BlogListMixins(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    CreateModlMixin : post 요청 받았을 때, 생성할 때 create하는 로직
    ListModelMixin : get 요청 받앗을 때, 목록 조회
    RetrieveModelMixin : get 요청 받았을 때, 상세 보기 조회
    UpdateModelMixin : put 또는 patch 요청 받았을 때, 수정
    DestroyModelMixin : delete 요청 받았을 때, 삭제
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request, date=datetime.now())


class BlogDetailMixins(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        return super().get_queryset()

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
