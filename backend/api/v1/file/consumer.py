from channels.generic.websocket import AsyncWebsocketConsumer

from api.v1.file.service.file_save import save_bytes


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.filesize = 0

        await self.accept()

    async def disconnect(self, close_code):
        ...

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            data = await self.text_receive(text_data)
        else:
            data = await self.bytes_receive(bytes_data)

    async def bytes_receive(self, raw_data):
        await save_bytes(raw_data, self.room_name, self.user_token, self.user_token)
        return False
