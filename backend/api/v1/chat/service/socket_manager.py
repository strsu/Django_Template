import channels.layers
from asgiref.sync import async_to_sync


class SocketManager:

    room_group_name = "prup" # socket에 연결된 group에 보낼 때 보내려는 group의 이름

    @classmethod
    def _group_send_(cls, data):
        """
        비동기 함수를 동기식으로 호출
        아래 함수를 호출하면 data 자체가 queue에 들어간다

        [ ] 내 local 함수에서 data.type의 info_message에 message를 넣어주는게 아니다
        [x] queue에 받은 메세지를 꺼낸 서버에서 type에 맞는 함수를 찾아서 message를 준다
            -> 때문에 서버에서 type에 맞는 함수가 없으면 소켓이 죽는다

        """
        try:
            async_to_sync(channels.layers.get_channel_layer().group_send)(
                cls.room_group_name, data
            )
        except Exception as e:
            """
            future: <Task finished name='Task-377' coro=<Connection.disconnect() done, defined at /usr/local/lib/python3.8/site-packages/redis/asyncio/connection.py:723> exception=RuntimeError('Event loop is closed')>
            Traceback (most recent call last):
            File "/usr/local/lib/python3.8/site-packages/redis/asyncio/connection.py", line 732, in disconnect
                self._writer.close()  # type: ignore[union-attr]
            File "/usr/local/lib/python3.8/asyncio/streams.py", line 353, in close
                return self._transport.close()
            File "/usr/local/lib/python3.8/asyncio/selector_events.py", line 692, in close
                self._loop.call_soon(self._call_connection_lost, None)
            File "/usr/local/lib/python3.8/asyncio/base_events.py", line 719, in call_soon
                self._check_closed()
            File "/usr/local/lib/python3.8/asyncio/base_events.py", line 508, in _check_closed
                raise RuntimeError('Event loop is closed')
            RuntimeError: Event loop is closed
            
            위 오류가 난다면, 
                [ ] "channels_redis.core.RedisChannelLayer",
                [x] "channels_redis.pubsub.RedisPubSubChannelLayer",
            RedisPubSubChannelLayer 를 사용하면 해결할 수 있다.

            위 오류가 여기 exception에서 잡히는 오류가 아니다!!
            """
            print(f"## - {e}")

    @classmethod
    def info(cls, message):
        data = {"type": "info_message", "data": message}
        cls._group_send_(data)
