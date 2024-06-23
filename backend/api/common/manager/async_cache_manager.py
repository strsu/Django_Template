from django.conf import settings

import redis as sync_redis
from redis import asyncio as aioredis  # python 3.11 이후 버전에서 aioredis 사라졌다.

import json
import logging

debug_logger = logging.getLogger("debug")


class AsyncCacheManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            f"redis://:{settings.BROKER_PASSWORD}@{settings.BROKER_URL}"
        )
        try:
            await self.redis.ping()
        except Exception as e:
            self.redis = None
            debug_logger.info(f"Cache 연결 실패!! - {e}")

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get_value(self, key):
        if not self.redis:
            return None

        try:
            value = await self.redis.get(key)
        except Exception as e:
            return None

        if value:
            return value.decode("utf-8")
        return None

    async def get_bytes_value(self, key):
        if not self.redis:
            return None

        try:
            value = await self.redis.get(key)
        except Exception as e:
            return None
        else:
            return value

    async def set_values(self, key, values):
        if not self.redis:
            return None

        try:
            await self.redis.set(key, values)
        except Exception as e:
            return None


class CacheManager:
    def __init__(self):
        self.redis = None

    def connect(self):
        self.redis = sync_redis.Redis(
            host=settings.BROKER_URL, password=settings.BROKER_PASSWORD
        )
        try:
            self.redis.ping()
        except Exception as e:
            self.redis = None
            debug_logger.info(f"Cache 연결 실패!! - {e}")

    def close(self):
        if self.redis:
            self.redis.close()

    def get_value(self, key):
        if not self.redis:
            print("asdf")
            return None

        try:
            value = self.redis.get(key)
        except Exception as e:
            print(e)
            return None
        else:
            return value

    def set_values(self, key, values):
        if not self.redis:
            return None

        try:
            self.redis.set(key, values)
        except Exception as e:
            return None

    # Redis 리스트에서 대기 중인 task들을 가져오기
    def get_tasks_in_queue(self, queue_key):
        tasks = []
        if self.redis:
            task_messages = self.redis.lrange(queue_key, 0, -1)
            for task_message in task_messages:
                task_info = json.loads(task_message)
                tasks.append(task_info)

        return tasks
