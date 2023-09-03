import aioredis


class userCounter:
    def __init__(self, cache_key):
        self.redis = None
        self.cache_key = cache_key

    async def connect(self):
        self.redis = await aioredis.from_url("redis://redis")
        # key_list = await self.redis.keys(f"{self.cache_key}*")

    async def close(self):
        self.redis.close()

    async def user_in(self):
        # Redis 캐시에서 데이터를 가져옵니다.
        count = await self.redis.get(self.cache_key)
        if not count:
            await self.redis.set(self.cache_key, 1)
            return 1
        else:
            await self.redis.set(self.cache_key, int(count.decode("utf-8")) + 1)

        return int(count.decode("utf-8")) + 1

    async def user_out(self):
        # Redis 캐시에서 데이터를 가져옵니다.
        count = await self.redis.get(self.cache_key)
        if not count:
            await self.redis.set(self.cache_key, 0)
            return 0
        else:
            await self.redis.set(self.cache_key, int(count.decode("utf-8")) - 1)

        return int(count.decode("utf-8")) - 1
