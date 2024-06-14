import channels.layers
from asgiref.sync import async_to_sync


class SocketManager:

    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.channel_layer = channels.layers.get_channel_layer()

    def group_send(self, data):
        # 비동기 함수를 동기식으로 호출
        async_to_sync(self.channel_layer.group_send)(self.channel_name, data)

    def get_group(self):
        # 비동기 함수를 동기식으로 호출
        print(dir(self.channel_layer))
        # return async_to_sync(self.channel_layer.group_get)(self.channel_name)
