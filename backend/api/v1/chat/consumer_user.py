from channels.generic.websocket import AsyncWebsocketConsumer
from config.settings_local import logger_info
import json
import random
import string

from api.v1.chat.service.food_recommand import foodRecommand
from api.v1.chat.service.user_counter import userCounter
from api.v1.chat.service.file_saver import save_image


# https://blog.logrocket.com/django-channels-and-websockets/
"""
    consumer의 코드반영은 바로 이루어 지지 않는다.
     -> websocket 특성이라는 것 같음
     
    그래서 코드를 반영하려면 dephan을 restart해줘야 한다.
    
    consumer는 사용자 마다 1개씩 부여되는 것 같다.
     -> 접속자 n 명 = consumer n개
    
    channel_layer = RedisChannelLayer
"""


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name = "mzoffice"
        self.user_name = self.scope["url_route"]["kwargs"]["user_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # logger_info.info(str(self.scope["headers"]))

        # 사용자 현황
        self.uc = userCounter(self.room_group_name)
        await self.uc.connect()

        # 음식 추천
        self.fr = foodRecommand()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.user_in()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.user_out()
        await self.uc.close()

    # Receive message from WebSocket
    async def receive(self, text_data=None):

        text_data_json = json.loads(text_data)
        data = {
            "type": "chat_message",
            "data": text_data_json["data"],
        }

        if text_data_json["data"]["image"]:
            save_image(text_data_json["data"]["image"], self.room_name)

        # Send message to room group - 나를 포함 모든 멤버
        if "오늘뭐먹지" in data["data"]["message"].replace(" ", ""):
            data = {
                "type": "food_message",
                "data": {
                    **text_data_json["data"],
                    "message": self.fr.get_random_store(),
                    "name": "음식추천해줌",
                    "token": "",
                },
            }

        """
            1. receive 가 호출됨
            2. type : chat_message
                -> chat_message 함수가 호출됨
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            data,
        )

    async def user_in(self):
        count = await self.uc.user_in()
        await self.send_user_count(count)

    async def user_out(self):
        count = await self.uc.user_out()
        await self.send_user_count(count)

    async def send_user_count(self, count):
        data = {
            "type": "info_message",
            "data": {"user_cnt": count},
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            data,
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"msg": event["data"]}))

    async def info_message(self, event):
        await self.send(text_data=json.dumps({"info": event["data"]}))

    async def food_message(self, event):
        await self.send(text_data=json.dumps({"food": event["data"]}))
