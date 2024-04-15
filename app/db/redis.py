from redis import asyncio as aioredis
from typing import Callable
from app.core.settings import Settings

from app.core.settings import settings


async def create_redis(settings: Settings) -> aioredis.Redis:
    """
    Create an asynchronous Redis connection using the provided settings.
    """
    return await aioredis.Redis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}"
    )


async def get_redis() -> aioredis.Redis:
    """
    Get a Redis connection session.
    """
    redis = await create_redis(settings)
    return redis


def get_redis_imp(
    redis_fn: Callable[[], aioredis.Redis]
) -> Callable[[], aioredis.Redis]:
    async def _get_redis() -> aioredis.Redis:
        return await redis_fn()

    return _get_redis
