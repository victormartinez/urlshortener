import random
import string
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

import settings
from infrastructure import logging
from urlshorten.app.exceptions import AppException, AppExceptionType
from urlshorten.app.shorten.data import (
    GetShortenedUrlRepository,
    PersistShortenedUrlRepository,
    ShortenedUrl,
    UpdateShortenedUrlRepository,
)
from urlshorten.db import cache
from urlshorten.db.session import get_session

logger = logging.get_logger(__name__)


async def _code_generator() -> str:
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(random.choices(chars, k=settings.URL_CODE_SIZE))  # nosec: B311


async def create(session: AsyncSession, destination_url: str) -> str:
    repository = PersistShortenedUrlRepository(session)
    for attempt_number in range(settings.URL_CODE_COLLISION_ATTEMPTS):
        try:
            code = await _code_generator()
            await repository.run(code=code, destination_url=destination_url)
            await cache.set_destination_url(code, destination_url)
            return code
        except AppException:
            logger.exception(
                "error shortening url",
                destination_url=destination_url,
                attempt=attempt_number,
            )

    raise AppException(
        type=AppExceptionType.INTEGRITY_ERROR,
        message="It was not possible to generate a code for the destination url.",
    )


async def update(
    session: AsyncSession,
    code: str,
    destination_url: Optional[str] = None,
    enabled: Optional[bool] = None,
) -> None:
    repository = UpdateShortenedUrlRepository(session)
    updated = await repository.run(code, destination_url, enabled)
    if not updated:
        raise AppException(
            type=AppExceptionType.ENTITY_NOT_FOUND,
            message=f"URL of code {code} was not updated.",
        )

    await cache.delete_destination_url(code)


async def retrieve(code: str) -> ShortenedUrl:  # type: ignore[return]
    destination_url, enabled = await cache.get_destination_url(code)
    if destination_url:
        return ShortenedUrl(
            code=code,
            destination_url=destination_url,
            enabled=enabled,
        )

    # gently reminder: just tries connection if cache miss
    async for session in get_session():
        repository = GetShortenedUrlRepository(session)
        await cache.set_destination_url(code, destination_url, enabled)
        return await repository.run(code=code)
