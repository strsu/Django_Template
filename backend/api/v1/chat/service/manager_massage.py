from channels.db import database_sync_to_async


class MessageManager:
    def __init__(self, room_name):
        self.room_name = room_name

    async def receive(self, data):
        ...

    @database_sync_to_async
    def __load_total_msg(self):
        ...

    @database_sync_to_async
    def save_msg(self, msg, name):
        from api.v1.chat.models import Group, Message

        try:
            group = Group.objects.get(name=self.room_name)
        except Exception as e:
            group = Group.objects.create(name=self.room_name)
            group.save()

        message = Message.objects.create(group=group, content=msg, name=name)
        message.save()
