from typing import Callable, Tuple

import aioredis

import settings
from infrastructure import logging

_redis_client = aioredis.from_url(settings.CACHE_URL)  # type: ignore[no-untyped-call]
_SEPARATOR_CHAR = "|"
logger = logging.get_logger(__name__)


def protect_connection(func: Callable) -> Callable:
    """Prevents application downtime if Redis down."""

    async def wrapped(*args, **kwargs):  # type: ignore[no-untyped-def]
        try:
            return await func(*args, **kwargs)
        except aioredis.exceptions.ConnectionError:
            logger.exception("redis connection error")

    return wrapped


@protect_connection
async def set_destination_url(
    code: str, destination_url: str, enabled: bool = True
) -> None:
    value = f"{destination_url}{_SEPARATOR_CHAR}{enabled}"
    await _redis_client.hset(settings.SHORTENED_URLS_HASH_NAME, code, value)


@protect_connection
async def get_destination_url(code: str) -> Tuple[str, bool]:
    result = await _redis_client.hget(settings.SHORTENED_URLS_HASH_NAME, code)
    if not result:
        return "", False
    return result.decode("utf-8").split(_SEPARATOR_CHAR)


@protect_connection
async def delete_destination_url(code: str) -> None:
    await _redis_client.hdel(settings.SHORTENED_URLS_HASH_NAME, code)
