import random
import string

from sqlalchemy.ext.asyncio import AsyncSession

import settings
from infrastructure import logging
from urlshorten.app.exceptions import AppException, AppExceptionType
from urlshorten.app.shorten.data import PersistShortenedUrlRepository

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
