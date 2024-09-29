from rest_framework import serializers

from .models import Goods, GoodsChatRoom, GoodsChatConversation


class GoodsChatRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, help_text="채팅방 id")
    to = serializers.UUIDField(help_text="상대방 uuid")
    last_msg = serializers.CharField(max_length=256, help_text="마지막 메세지 내용")
    last_msg_time = serializers.DateTimeField(help_text="마지막 메세지 송수신 시각")
    owner_last_read_at = serializers.DateTimeField(
        help_text="빌려주는 사람의 마지막 확인 시각"
    )
    buyer_last_read_at = serializers.DateTimeField(
        help_text="빌리는 사람의 마지막 확인 시각"
    )

    def to_representation(self, instance):
        user = self.context["request"].user
        last_conversation = (
            GoodsChatConversation.objects.filter(room=instance)
            .order_by("-timestamp")
            .first()
        )

        ret = {
            "opponent": {"type": "buyer", "username": instance.buyer.username},
        }
        if user == instance.buyer:
            ret = {
                "opponent": {
                    "type": "seller",
                    "username": instance.product.owner.username,
                },
            }

        ret = {
            **ret,
            "id": instance.id,
            "product": {
                "id": instance.product.id,
                "title": instance.product.title,
                "image": instance.product.image.url,
            },
            "last_msg": last_conversation.get_message() if last_conversation else None,
            "last_msg_time": last_conversation.get_kst() if last_conversation else None,
            "owner_last_read_at": instance.owner_last_read_at,
            "buyer_last_read_at": instance.buyer_last_read_at,
        }

        return ret


class GoodsChatConversationSerializer(serializers.Serializer):
    is_my = serializers.BooleanField()
    timestamp = serializers.DateTimeField()
    message = serializers.CharField(max_length=256)
    type = serializers.ChoiceField(choices=GoodsChatConversation.MessageType.choices)

    def to_representation(self, instance):

        is_my = False
        user = self.context["request"].user
        if instance.room.buyer == user:
            # 로그인 사용자가 빌리는 사람이면
            if instance.is_guest:
                # is_guest=True인 메세지가 자신이 보낸 메세지
                is_my = True
        else:
            # 로그인 사용자가 빌려주는 사람이면
            if not instance.is_guest:
                # is_guest=False인 메세지가 자신이 보낸 메세지
                is_my = True

        return {
            # "timestamp": instance.get_kst(),
            "timestamp": instance.timestamp,
            "message": instance.message,
            "type": instance.type,
            "is_my": is_my,
        }
