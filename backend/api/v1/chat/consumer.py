import json
from channels.generic.websocket import AsyncWebsocketConsumer

# https://blog.logrocket.com/django-channels-and-websockets/


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if message:
            text = message["text"]
            await self.send_to_other_members(text)

        return

        # Send message to room group - 나를 포함 모든 멤버
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def send_to_other_members(self, message):
        members = await self.get_group_members(self.group_name)
        for member in members:
            f = open("/opt/text.log", "a", encoding="utf-8")
            f.write(member + "\n")
            f.close()
            if member != self.channel_name:
                await self.channel_layer.send(
                    member,
                    {
                        "type": "chat_message",
                        "message": message,
                    },
                )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @staticmethod
    async def get_group_members(group_name):
        """
        Get list of members from the channel layer for a specific group
        """
        channel_layer = ChatConsumer.channel_layer
        group = await channel_layer.group_get(group_name)
        if group:
            return group.keys()
        else:
            return []
