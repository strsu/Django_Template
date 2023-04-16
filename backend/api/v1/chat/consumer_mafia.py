from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import os
import json
import random
import string
import copy
from datetime import datetime

from api.v1.chat.service.food_recommand import foodRecommand
from api.v1.chat.service.user_counter import userCounter
from api.v1.chat.service.file_saver import save_base64, save_bytes

#

from config.settings.base import STATIC_ROOT
from config.settings.base import logger_info


# https://blog.logrocket.com/django-channels-and-websockets/
"""
    consumer의 코드반영은 바로 이루어 지지 않는다.
     -> websocket 특성이라는 것 같음
     
    그래서 코드를 반영하려면 dephan을 restart해줘야 한다.
    
    consumer는 사용자 마다 1개씩 부여되는 것 같다.
     -> 접속자 n 명 = consumer n개
    
    channel_layer = RedisChannelLayer
"""


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


class MafiaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "mafia"
        self.room_group_name = "game_%s" % self.room_name
        self.user_token = generate_random_string(10)
        self.my_role = ""

        # logger_info.info(str(self.scope["headers"]))

        # 사용자 현황
        self.uc = userCounter(self.room_group_name)
        await self.uc.connect()

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
    async def receive(self, text_data=None, bytes_data=None):
        """
        receive는 data를 전송한 consumer만 실행되는 것 같다.
        이후에 아래서 정리된 data가 redis에 올라가고
        data를 받아야 하는 그룹원들은
        redis에 올라온 data를 가져와 type에 명시된 함수를 실행하는 것 같다.
        """

        data = await self.text_receive(text_data)

        if data:
            data["data"]["token"] = self.user_token

            await self.channel_layer.group_send(
                self.room_group_name,
                data,
            )

    async def text_receive(self, raw_data):
        text_data_json = json.loads(raw_data)
        data = {
            "type": "chat_message",
            "data": text_data_json["data"],
        }

        return data

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

    async def hello(self):
        data = {
            "type": "info_message",
            "data": {"user_token": self.user_token},
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            data,
        )

    async def chat_message(self, event):

        data = copy.deepcopy(event["data"])
        if data["token"] == self.user_token:
            data["flag"] = True
        else:
            data["flag"] = False
        del data["token"]

        await self.send(text_data=json.dumps({"msg": data}))

    async def info_message(self, event):
        await self.send(text_data=json.dumps({"info": event["data"]}))

    @database_sync_to_async
    def set_file(self, path, name, code):
        from api.v1.file.models import File

        file = File.objects.create(path=path, name=name, code=code)
        file.save()
