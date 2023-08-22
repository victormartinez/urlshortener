import random
import string
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

import settings
from infrastructure import logging
from urlshorten.app.shorten.data import (
    GetShortenedUrlRepository,
    PersistShortenedUrlRepository,
    ShortenedUrl,
    UpdateShortenedUrlRepository,
)
from urlshorten.db import cache
from urlshorten.db.session import get_session

logger = logging.get_logger(__name__)


async def create(session: AsyncSession, destination_url: str) -> str:
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    code = "".join(random.choices(chars, k=settings.URL_CODE_SIZE))  # nosec: B311
    repository = PersistShortenedUrlRepository(session)
    await repository.run(code=code, destination_url=destination_url)
    await cache.set_destination_url(code, destination_url)
    return code


async def update(
    session: AsyncSession,
    code: str,
    *,
    destination_url: Optional[str] = None,
    enabled: Optional[bool] = None,
) -> int:
    repository = UpdateShortenedUrlRepository(session)
    updated = await repository.run(
        code, 
        destination_url=destination_url,
        enabled=enabled
    )
    if updated:
        await cache.delete_destination_url(code)
    return updated


async def retrieve(code: str) -> Optional[ShortenedUrl]:  # type: ignore[return]
    destination_url, enabled = await cache.get_destination_url(code)
    if not destination_url:
        # gently reminder: just tries connection if cache miss
        async for session in get_session():
            repository = GetShortenedUrlRepository(session)
            result: Optional[ShortenedUrl] = await repository.run(code=code)
            if not result:
                return None

            destination_url, enabled = result.destination_url, result.enabled

    await cache.set_destination_url(code, destination_url, enabled)
    return ShortenedUrl(
        code=code,
        destination_url=destination_url,
        enabled=enabled,
    )
