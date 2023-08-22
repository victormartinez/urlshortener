from tests.suite.factory import DBShortenedUrlFactoryData
from tests.suite.database import DatabaseUtils
from urlshorten.db import DBShortenedUrl
from urlshorten.app.shorten.data import (
    UpdateShortenedUrlRepository, 
    GetShortenedUrlRepository,
    ShortenedUrl,
)


async def test_update_shortened_url_destination_url_and_enabled(session):
    CODE = "h4rry"
    OLD_DESTINATION_URL = "https://mercadolivre.com"
    NEW_DESTINATION_URL = "https://google.com"
    db_object: DBShortenedUrl = DBShortenedUrlFactoryData.build(
        code=CODE, destination_url=OLD_DESTINATION_URL
    )
    await DatabaseUtils.create(session, db_object)
    assert db_object.code == CODE
    assert db_object.destination_url == OLD_DESTINATION_URL
    assert db_object.enabled is True

    update_repository = UpdateShortenedUrlRepository(session)
    rowcount = await update_repository.run(
        code=db_object.code, destination_url=NEW_DESTINATION_URL, enabled=False
    )
    assert rowcount == 1

    get_repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await get_repository.run(code=CODE)

    assert result.code == CODE
    assert result.destination_url == NEW_DESTINATION_URL
    assert result.enabled is False


async def test_update_shortened_url_destination_url(session):
    CODE = "p0tt3r"
    OLD_DESTINATION_URL = "https://bing.com"
    NEW_DESTINATION_URL = "https://google.com"
    db_object: DBShortenedUrl = DBShortenedUrlFactoryData.build(
        code=CODE, destination_url=OLD_DESTINATION_URL
    )
    await DatabaseUtils.create(session, db_object)
    assert db_object.code == CODE
    assert db_object.destination_url == OLD_DESTINATION_URL
    assert db_object.enabled is True

    update_repository = UpdateShortenedUrlRepository(session)
    rowcount = await update_repository.run(
        code=db_object.code, destination_url=NEW_DESTINATION_URL
    )
    assert rowcount == 1

    get_repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await get_repository.run(code=CODE)

    assert result.code == CODE
    assert result.destination_url == NEW_DESTINATION_URL
    assert result.enabled is True


async def test_update_shortened_url_enabled(session):
    CODE = "h0gw4rts"
    DESTINATION_URL = "https://bing.com"
    db_object: DBShortenedUrl = DBShortenedUrlFactoryData.build(
        code=CODE, destination_url=DESTINATION_URL
    )
    await DatabaseUtils.create(session, db_object)
    assert db_object.code == CODE
    assert db_object.destination_url == DESTINATION_URL
    assert db_object.enabled is True

    update_repository = UpdateShortenedUrlRepository(session)
    rowcount = await update_repository.run(code=db_object.code, enabled=False)
    assert rowcount == 1

    get_repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await get_repository.run(code=CODE)

    assert result.code == CODE
    assert result.destination_url == DESTINATION_URL
    assert result.enabled is False


async def test_update_shortened_url_enabled_none(session):
    CODE = "h0gw4rts"
    OLD_DESTINATION_URL = "https://bing.com"
    NEW_DESTINATION_URL = "https://google.com"
    db_object: DBShortenedUrl = DBShortenedUrlFactoryData.build(
        code=CODE, destination_url=OLD_DESTINATION_URL
    )
    await DatabaseUtils.create(session, db_object)
    assert db_object.code == CODE
    assert db_object.destination_url == OLD_DESTINATION_URL
    assert db_object.enabled is True

    update_repository = UpdateShortenedUrlRepository(session)
    rowcount = await update_repository.run(
        code=db_object.code,
        destination_url=NEW_DESTINATION_URL,
        enabled=None,
    )
    assert rowcount == 1

    get_repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await get_repository.run(code=CODE)

    assert result.code == CODE
    assert result.destination_url == NEW_DESTINATION_URL
    assert result.enabled is True


async def test_update_shortened_url_no_attrs(session):
    update_repository = UpdateShortenedUrlRepository(session)
    rowcount = await update_repository.run(code="gr1ng0tts")
    assert rowcount == 0


async def test_update_shortened_url_not_found(session):
    update_repository = UpdateShortenedUrlRepository(session)
    rowcount = await update_repository.run(code="F4k3", destination_url="https://")
    assert rowcount == 0