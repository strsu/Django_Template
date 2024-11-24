from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from django.utils import timezone
from django.db.models import Prefetch

from config.exceptions.custom_exceptions import CustomException

from .models import GoodsChatRoom, GoodsChatConversation
from .serializer import GoodsChatRoomSerializer, GoodsChatConversationSerializer


@extend_schema_view(
    get=extend_schema(
        summary="채팅방",
    ),
)
class ChatRoomListView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    serializer_class = GoodsChatRoomSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return GoodsChatRoom.get_rooms(user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(
        summary="채팅메세지",
        parameters=[
            OpenApiParameter(
                name="timestamp",
                description="해당 timestamp 이전에 온 최근 100개 메세지",
                default=timezone.now(),
                required=False,
                type=OpenApiTypes.DATETIME,
            ),
        ],
    ),
)
class ChatConversationListView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    serializer_class = GoodsChatConversationSerializer
    pagination_class = None

    def get_queryset(self):
        """
        NOTE - prefetch 안에서 select_related 는 쓰지 말자
            각 쿼리마다 select를 보내서, 오히려 쿼리개수가 늘어간다
        """
        user = self.request.user
        room = (
            GoodsChatRoom.actives.select_related("product", "buyer")
            .prefetch_related(
                Prefetch(
                    "goodschatconversation_set",
                    queryset=GoodsChatConversation.objects.all().order_by("-timestamp"),
                )
            )
            .get(id=self.kwargs.get("pk"))
        )
        if room.buyer != user and room.product.owner != user:
            raise CustomException()
        timestamp = self.request.GET.get("timestamp")
        return room.get_messages(timestamp)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={"request": request})

        ## 마지막 확인시간 갱신
        room = GoodsChatRoom.actives.get(id=self.kwargs.get("pk"))
        if room.buyer == request.user:
            room.buyer_last_read_at = timezone.now()
        else:
            room.owner_last_read_at = timezone.now()
        room.save()

        return Response(serializer.data[::-1])


@extend_schema_view(
    post=extend_schema(
        summary="채팅방 생성",
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"room": {"type": "integer", "example": 1}},
                },
                description="성공 응답",
            ),
            400: OpenApiResponse(description="자신과의 채팅방은 생성할 수 없습니다."),
            404: OpenApiResponse(description="상품을 찾을 수 없습니다."),
        },
    )
)
class CreateChatRoom(APIView):

    def post(self, request, *args, **kwargs):
        chat_room, created = GoodsChatRoom.objects.get_or_create(product_id=kwargs.get("pk"), buyer=request.user)

        return Response({"room": chat_room.id}, status=201)
