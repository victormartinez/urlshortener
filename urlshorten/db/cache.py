from typing import Tuple

import aioredis

import settings

_redis_client = aioredis.from_url(settings.CACHE_URL)  # type: ignore[no-untyped-call]
_SEPARATOR_CHAR = "|"


async def set_destination_url(
    code: str, destination_url: str, enabled: bool = True
) -> None:
    value = f"{destination_url}{_SEPARATOR_CHAR}{enabled}"
    await _redis_client.hset(settings.SHORTENED_URLS_HASH_NAME, code, value)


async def get_destination_url(code: str) -> Tuple[str, bool]:
    result = await _redis_client.hget(settings.SHORTENED_URLS_HASH_NAME, code)
    if not result:
        return "", False
    return result.split(_SEPARATOR_CHAR)


async def delete_destination_url(code: str) -> None:
    await _redis_client.hdel(settings.SHORTENED_URLS_HASH_NAME, code)
