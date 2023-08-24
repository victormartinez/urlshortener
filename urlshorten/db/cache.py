from typing import Callable, Tuple, Optional

import aioredis

import settings
from infrastructure import logging

_redis = aioredis.from_url(settings.CACHE_URL)  # type: ignore[no-untyped-call]
_SEPARATOR_CHAR = "|"
logger = logging.get_logger(__name__)


def protect_connection(func: Callable) -> Callable:
    """Prevents application downtime if Redis down."""

    async def wrapped(*args, **kwargs):  # type: ignore[no-untyped-def]
        try:
            return await func(*args, **kwargs)
        except aioredis.exceptions.RedisError:
            logger.exception("redis error")
            return None

    return wrapped


@protect_connection
async def set_destination_url(
    code: str, destination_url: str, enabled: bool = True
) -> None:
    async with _redis.client() as conn:
        value = f"{destination_url.strip()}{_SEPARATOR_CHAR}{enabled}"
        await conn.hset(settings.SHORTENED_URLS_HASH_NAME, code, value)


@protect_connection
async def get_destination_url(code: str) -> Optional[Tuple[str, bool]]:
    async with _redis.client() as conn:
        result = await conn.hget(settings.SHORTENED_URLS_HASH_NAME, code.strip())
        if not result:
            return "", False
        return result.decode("utf-8").split(_SEPARATOR_CHAR)


@protect_connection
async def delete_destination_url(code: str) -> None:
    async with _redis.client() as conn:
        await conn.hdel(settings.SHORTENED_URLS_HASH_NAME, code.strip())
