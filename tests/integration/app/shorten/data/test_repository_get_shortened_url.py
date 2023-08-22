from tests.suite.database import DatabaseUtils
from tests.suite.factory import DBShortenedUrlFactoryData
from urlshorten.app.shorten.data import GetShortenedUrlRepository, ShortenedUrl
from urlshorten.db import DBShortenedUrl


async def test_get_shortened_url(session):
    db_object: DBShortenedUrl = DBShortenedUrlFactoryData.build()
    await DatabaseUtils.create(session, db_object)

    repository = GetShortenedUrlRepository(session)
    result: ShortenedUrl = await repository.run(code=db_object.code)

    assert result.code == db_object.code
    assert result.destination_url == db_object.destination_url
    assert result.enabled == db_object.enabled


async def test_get_shortened_url_not_found(session):
    repository = GetShortenedUrlRepository(session)
    result = await repository.run(code="F4k3C0d3")

    assert result is None
