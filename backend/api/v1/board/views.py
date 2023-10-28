from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
)
from rest_framework.response import Response

# filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from . import filters as custom_filters

from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission, User

from config.exceptions.custom_exceptions import CustomParameterException

from api.v1.board.models import Board, BoardCategory, BoardComment, BoardMedia
from api.v1.board.serializer import BoardSerializer, BoardCommentSerializer

from api.common.utils import save_base64, read_base64


class BoardView(viewsets.ModelViewSet, PermissionRequiredMixin):
    queryset = Board.actives.all()
    serializer_class = BoardSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]  # DjangoFilterBackend 지정, OrderingFitering 지정
    filterset_class = custom_filters.BoardFilter
    # filterset_fields = ["comment__author"]  # filtering 기능을 사용할 field 입력
    ordering_fields = ["author", "category"]  # 정렬 대상이 될 field 지정
    ordering = ["author"]  # Default 정렬 기준 지정

    permission_classes = [DjangoModelPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=204)


class BoardCommentdView(viewsets.ModelViewSet):
    queryset = BoardComment.actives.all()
    serializer_class = BoardCommentSerializer

    permission_classes = [AllowAny]

    lookup_field = "pk"

    def check_board_actives(self):
        board_id = self.kwargs.get("b_id")
        try:
            Board.actives.get(id=board_id)
        except Exception as e:
            raise Exception("게시물을 찾을 수 없습니다.")

    def get_serializer_class(self):
        self.check_board_actives()
        return self.serializer_class

    def get_queryset(self):
        self.check_board_actives()
        board_id = self.kwargs.get("b_id")
        return super().get_queryset().filter(board_id=board_id)

    def get_object(self):
        self.check_board_actives()
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=204)


class BoardLikeView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, b_id):
        user = request.user

        if user.is_anonymous:
            raise Exception("게시물 추천은 회원만 할 수 있습니다.")

        try:
            board = Board.actives.get(id=b_id)
        except Exception as e:
            raise Exception("게시물을 찾을 수 없습니다.")
        else:
            board.toggle_like(user)

        return Response(status=200)


class BoardCommentLikeView(APIView):
    permission_classes = [AllowAny]

    def check_board_actives(self):
        board_id = self.kwargs.get("b_id")
        try:
            Board.actives.get(id=board_id)
        except Exception as e:
            raise Exception("게시물을 찾을 수 없습니다.")

    def put(self, request, b_id, c_id):
        self.check_board_actives()

        user = request.user

        if user.is_anonymous:
            raise Exception("댓글 추천은 회원만 할 수 있습니다.")

        try:
            comment = BoardComment.actives.get(id=c_id, board_id=b_id)
        except Exception as e:
            raise Exception("댓글을 찾을 수 없습니다.")
        else:
            comment.toggle_like(user)

        return Response(status=200)


class BoardImageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, b_id):
        images = []

        try:
            board = Board.actives.get(id=b_id)
        except Exception as e:
            raise Exception("게시물을 찾을 수 없습니다.")
        else:
            filenames = BoardMedia.actives.filter(board=board).values_list(
                "filename", flat=True
            )

            for filename in filenames:
                image = read_base64(filename)
                images.append({"image": image, "filename": filename})

        return Response(data=images, status=200)

    def post(self, request, b_id):
        try:
            board = Board.actives.get(id=b_id)
        except Exception as e:
            raise Exception("게시물을 찾을 수 없습니다.")
        else:
            image = request.data.get("image")
            filename = request.data.get("filename")

            if image is None:
                raise Exception("사진을 넣어주세요")

            if filename is None:
                raise Exception("파일 이름을 넣어주세요")

            save_base64(image, filename)

            BoardMedia.actives.create(board=board, filename=filename)

        return Response(status=201)
