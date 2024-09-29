from api.common.managers.async_cache_manager import AsyncCacheManager


class userCounter:
    def __init__(self, cache_key):
        self.redis = AsyncCacheManager()
        self.cache_key = cache_key

    async def connect(self):
        self.redis.connect()

    async def close(self):
        self.redis.close()

    async def user_in(self):
        # Redis 캐시에서 데이터를 가져옵니다.
        count = await self.redis.get_value(self.cache_key)
        if not count:
            await self.redis.set_value(self.cache_key, 1)
            return 1
        else:
            count = count.decode()
            await self.redis.set_value(self.cache_key, int(count) + 1)

        return int(count) + 1

    async def user_out(self):
        # Redis 캐시에서 데이터를 가져옵니다.
        count = await self.redis.get_value(self.cache_key)
        if not count:
            await self.redis.set_value(self.cache_key, 0)
            return 0
        else:
            count = count.decode()
            await self.redis.set_value(self.cache_key, int(count) - 1)

        return int(count) - 1
