from channels.db import database_sync_to_async


class MessageManager:
    def __init__(self, room_name):
        self.room_name = room_name
        self.group = None

    async def receive(self, data): ...

    @database_sync_to_async
    def __load_total_msg(self): ...

    @database_sync_to_async
    def save_msg(self, msg, name):
        from api.v1.chat.models import Group, Message

        try:
            self.group = Group.objects.get(name=self.room_name)
        except Exception as e:
            self.group = Group.objects.create(name=self.room_name)

        message = Message.objects.create(group=self.group, content=msg, name=name)
        message.save()
