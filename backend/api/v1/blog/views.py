from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import StreamingHttpResponse

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

from config.exceptions.custom_exceptions import CustomException

from api.v1.blog.models import Blog
from api.v1.blog.serializer import BlogSerializer

from datetime import datetime
import time


class BlogApiView(APIView):
    # permission_classes = [IsAuthenticated] # 전역으로 설정되어 있어서 굳이 또 넣을 필요는 없다.
    # permission_classes = [AllowAny] # Auth가 전역으로 되어 있어서 해당 view에 Auth를 없애려면 이렇게 넣어주면 된다.
    authentication_classes = (JWTAuthentication, BasicAuthentication)

    ## drf_yasg
    # @swagger_auto_schema(
    #     operation_id="시스템설정 옵션 조희",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             "id",
    #             openapi.IN_QUERY,
    #             description="api/v1/blog/",
    #             required=True,
    #             type=openapi.TYPE_STRING,
    #         ),
    #     ],
    #     responses={
    #         "200": openapi.Response(
    #             description="요청 성공",
    #             examples={
    #                 "application/json": {
    #                     "results": {
    #                         "generation_hour": "05-21",
    #                     }
    #                 },
    #             },
    #         ),
    #         "400": openapi.Response(
    #             description="잘못된 요청",
    #             examples={"application/json": {"message": "요청 실패"}},
    #         ),
    #     },
    # )
    def get(self, request):
        if not ("id" in request.GET):
            raise CustomException(detail="게시글을 찾을 수 없습니다", code=404)

        id = request.GET.get("id")
        data = Blog.objects.get(id=id)
        serializer = BlogSerializer(instance=data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     operation_id="블로그",
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             "content": openapi.Schema(
    #                 type=openapi.TYPE_STRING, description="글 내용"
    #             ),
    #             "tags": openapi.Schema(type=openapi.TYPE_STRING, description="글 태그"),
    #         },
    #     ),
    #     responses={
    #         "200": BlogSerializer,
    #         "400": openapi.Response(
    #             description="잘못된 요청",
    #             examples={"application/json": {"message": "요청 실패"}},
    #         ),
    #     },
    # )
    def post(self, request):
        """
        request.data에
            content, tags 있어야한다.
            date, user는 back에서 설정
        """
        deserializer = BlogSerializer(data=request.data)
        if deserializer.is_valid():
            # user는 다음과 같이 설정할 수 있다.
            # serializer내 field에서 date를 지우고 여기서 넣어주면 된다!!
            deserializer.save(user=request.user, date=datetime.now())
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=400)


class BlogListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    CreateModelMixin : post 요청 받았을 때, 생성할 때 create하는 로직
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


class BlogStreamView(APIView):
    def get(self, request):
        # 스트리밍할 데이터를 생성하는 제너레이터 함수
        def event_stream():
            for i in range(1, 6):
                yield f"data: Message {i}\n\n"  # 데이터를 전송할 때마다 줄바꿈을 포함해야 합니다.
                time.sleep(1)  # 데이터를 1초 간격으로 보냄

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        return response
