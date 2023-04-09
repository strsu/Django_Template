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


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name = "mzoffice"
        self.user_name = self.scope["url_route"]["kwargs"]["user_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user_token = generate_random_string(10)
        self.filesize = 0
        self.path = os.path.join(STATIC_ROOT, f"chat/img/{self.room_name}")

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
    async def receive(self, text_data=None, bytes_data=None):
        """
        receive는 data를 전송한 consumer만 실행되는 것 같다.
        이후에 아래서 정리된 data가 redis에 올라가고
        data를 받아야 하는 그룹원들은
        redis에 올라온 data를 가져와 type에 명시된 함수를 실행하는 것 같다.
        """

        if text_data is not None:
            data = await self.text_receive(text_data)
        else:
            data = await self.bytes_receive(bytes_data)

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

        if "flag" in text_data_json["data"]:
            flag = text_data_json["data"]["flag"]
            filename = text_data_json["data"]["file"]
            if "filesize" in text_data_json["data"]:
                self.filesize = text_data_json["data"]["filesize"]
            save_filename = await save_bytes(
                None, self.room_name, flag, self.user_token, filename
            )
            await self.send_current_percentage()

            if not flag:
                code = generate_random_string(4)
                await self.set_file(f"{self.room_name}/{save_filename}", filename, code)

                data["data"]["name"] = "업로드 해줌"
                data["data"]["message"] = f"업로드 완료, 다운로드 코드: {code}"
                await self.send(text_data=json.dumps({"msg": data["data"]}))

            return False
        elif "image" in text_data_json["data"]:
            save_base64(text_data_json["data"]["image"], self.room_name)
        elif "오늘뭐먹지" in data["data"]["message"].replace(" ", ""):
            # Send message to room group - 나를 포함 모든 멤버
            data = {
                "type": "food_message",
                "data": {
                    **text_data_json["data"],
                    "message": self.fr.get_random_store(),
                    "name": "음식추천해줌",
                    "token": "",
                },
            }

        return data

    async def bytes_receive(self, raw_data):
        await self.send_current_percentage()
        await save_bytes(raw_data, self.room_name, 2, self.user_token, self.user_token)
        return False

    async def send_current_percentage(self):
        try:
            file_size = os.path.getsize(os.path.join(self.path, self.user_token))
            percent = round((file_size / self.filesize) * 100, 3)
        except Exception as e:
            percent = 100
        data = {"percent": percent}
        await self.send(text_data=json.dumps({"info": data}))

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
        # consumer와 연결된 사용자한테 데이터를 전송해준다.
        # 내부적으로 token을 검사해서, flag로 변경시킨다.
        """
        들어온 순서대로 data가 전송된다.
        들어온 data는 연결된 user에게 전송된 후
        다시 redis로 들어간다.
            -> 이건 정확한 로직을 모르겠다.
        그래서 전송하면서 각 user의 consumer가 data를 변조하면
        이 그후에 값을 받는 사용자들은 변조된 값을 받게 된다.
            -> 그럼 redis에서 가져온 객체를 사용하지 않고,
            -> deepcopy를 해서 사용하면 원본 객체는 손상시키지 않기 때문에
            -> 숨기고 싶은 데이터를 숨길 수 있다.

        또한 3번 user가 보낸 data는 3번 유저가 먼저 받는게 아니라
        1, 2번 유저가 받고 그 이후에 3번 유저가 data를 받게 된다.
        """

        data = copy.deepcopy(event["data"])
        if data["token"] == self.user_token:
            data["flag"] = True
        else:
            data["flag"] = False
        del data["token"]

        await self.send(text_data=json.dumps({"msg": data}))

    async def info_message(self, event):
        await self.send(text_data=json.dumps({"info": event["data"]}))

    async def food_message(self, event):
        if "token" in event["data"]:
            del event["data"]["token"]
        await self.send(text_data=json.dumps({"food": event["data"]}))

    """
    async def connect(self):
        #이건 처음 연결되자 마자 실행되는 함수이다.
        
      pass

        # self.username = await database_sync_to_async(self.set_file)()
        # await self.set_file()
    """

    @database_sync_to_async
    def set_file(self, path, name, code):
        from api.v1.file.models import File

        file = File.objects.create(path=path, name=name, code=code)
        file.save()
