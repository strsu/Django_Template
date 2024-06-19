import channels.layers
from asgiref.sync import async_to_sync


class SocketManager:

    channel_name = "prup"

    @property
    def channel_name():
        pass

    @classmethod
    def _group_send_(cls, data):
        """
        비동기 함수를 동기식으로 호출
        아래 함수를 호출하면 data 자체가 queue에 들어간다

        [ ] 내 local 함수에서 data.type의 info_message에 message를 넣어주는게 아니다
        [x] queue에 받은 메세지를 꺼낸 서버에서 type에 맞는 함수를 찾아서 message를 준다
            -> 때문에 서버에서 type에 맞는 함수가 없으면 소켓이 죽는다

        """
        async_to_sync(channels.layers.get_channel_layer().group_send)(
            cls.channel_name, data
        )

    @classmethod
    def info(cls, message):
        data = {"type": "info_message", "data": message}
        cls._group_send_(data)
