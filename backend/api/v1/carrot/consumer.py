from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from asgiref.sync import sync_to_async

from django.utils import timezone

from api.common.managers.async_cache_manager import AsyncCacheManager

import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "carrot"

        self.user = self.scope["user"]
        self.redis = None

        if self.user is None:
            await self.close(4004)
        else:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_add(self.user.uuid, self.channel_name)
            await self.accept()

            self.redis = AsyncCacheManager()
            await self.redis.connect()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.user.uuid, self.channel_name)

        if self.redis:
            await self.redis.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")
            data = text_data_json.get("data", {})

            if message_type == "message":
                await self.handle_message(data)
            elif message_type == "health":
                await self.handle_health()
            elif message_type == "typing":
                await self.handle_typing(data)
            else:
                logger.warning(f"Unknown message type: {message_type}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
        except KeyError as e:
            logger.error(f"Missing expected key: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")

    async def handle_message(self, data):
        try:
            kst = await self.save_message(data["room"], data["msg"])

            uuid_dict = await self.get_room(data["room"])
            msg_data = {
                "type": "send_group",
                "data": {
                    "type": "message",
                    "data": {
                        "room": data["room"],
                        "msg": {
                            "timestamp": kst,
                            "message": data["msg"],
                            "is_my": False,
                            "type": 1,
                        },
                    },
                },
            }

            uuid = None
            for key, _uuid in uuid_dict.items():
                if _uuid != str(self.user.uuid):
                    uuid = _uuid
                    break

            if uuid:
                is_active = await self.check_user_active(uuid)

                if is_active:
                    await self.channel_layer.group_send(uuid, msg_data)
                else:
                    print("사용자 비접속")

        except KeyError as e:
            logger.error(f"Message data missing key: {e}")

    async def handle_health(self):
        self.redis.set_value(f"last_active_{self.user.uuid}", timezone.now())
        await self.send(text_data=json.dumps({"type": "health"}))

    async def handle_typing(self, data):
        try:
            typing_data = {
                "type": "typing",
                "data": {
                    "room": data["room"],
                    "from": self.user.uuid,
                },
            }
            await self.channel_layer.group_send(data["to"], typing_data)
        except KeyError as e:
            logger.error(f"Typing data missing key: {e}")

    @database_sync_to_async
    def save_message(self, room, msg):
        from api.v1.carrot.models import GoodsChatConversation

        msg = GoodsChatConversation(
            room_id=room,
            message=msg,
            type=GoodsChatConversation.MessageType.TEXT,
        )
        msg.save(self.user)

        return msg.get_kst()

    async def get_room(self, room_id):
        """
        redis에 orm은 저장을 못 한다.
        """
        uuid_dict = await self.redis.get_value(f"room_{room_id}")

        if uuid_dict is None:
            room = await self.get_room_from_db(room_id)

            buyer = await sync_to_async(lambda: room.buyer)()
            owner = await sync_to_async(lambda: room.product.owner)()

            uuid_dict = {"buyer": str(buyer.uuid), "owner": str(owner.uuid)}

            await self.redis.set_value(f"room_{room_id}", json.dumps(uuid_dict))
        else:
            uuid_dict = json.loads(uuid_dict)

        return uuid_dict

    @database_sync_to_async
    def get_room_from_db(self, room_id):
        from api.v1.carrot.models import GoodsChatRoom

        try:
            room = GoodsChatRoom.objects.get(id=room_id)
        except GoodsChatRoom.DoesNotExist:
            return False
        else:
            return room

    async def check_user_active(self, uuid):
        return await self.redis.execute_command(f"PUBSUB CHANNELS asgi__group__{uuid}")

    async def send_group(self, event):
        """
        await self.channel_layer.group_send(target_layer, data)

        NOTE - 이 함수는 보낸사람의 프로세스에서 실행되는 함수가 아니다.
        target_layer의 프로세스에서 실행되는 함수다.

        때문에 target_layer가 없다면 이 함수는 실행되지 않는다.
            -> socket_manager 와 동일한 원리

        즉
            A -> B 전송
                B의 프로세스에서 send_group이 호출됨

        """
        data = event.get("data")
        await self.send(text_data=json.dumps(data))
