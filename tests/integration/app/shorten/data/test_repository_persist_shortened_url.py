import pytest

from urlshorten.app.exceptions import AppException, AppExceptionType
from urlshorten.app.shorten.data import (
    GetShortenedUrlRepository,
    PersistShortenedUrlRepository,
    ShortenedUrl,
)


async def test_persist_shortened_url(session):
    CODE, DESTINATION = "a1B2c3", "https://google.com"

    repository = PersistShortenedUrlRepository(session)
    await repository.run(code=CODE, destination_url=DESTINATION)

    repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await repository.run(code=CODE)

    assert result.code == CODE
    assert result.destination_url == DESTINATION
    assert result.enabled is True


async def test_persist_shortened_url_integrity_error(session):
    CODE, DESTINATION = "b2c3d4", "https://bing.com"

    persist_repository = PersistShortenedUrlRepository(session)
    await persist_repository.run(code=CODE, destination_url=DESTINATION)

    get_repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await get_repository.run(code=CODE)
    assert result is not None

    with pytest.raises(AppException) as excinfo:
        await persist_repository.run(code=CODE, destination_url="http://google.com")

    assert excinfo.value.type == AppExceptionType.INTEGRITY_ERROR
