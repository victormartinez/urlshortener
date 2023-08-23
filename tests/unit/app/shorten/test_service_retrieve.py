from unittest import mock

import pytest

from urlshorten.app import shorten
from urlshorten.app.shorten.data import ShortenedUrl


@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_retrieve_from_cache(cache_mock):
    CODE, DESTINATION, ENABLED = "FAKECODE", "https://google.com", True
    cache_mock.get_destination_url.return_value = DESTINATION, ENABLED
    result = await shorten.retrieve(CODE)

    assert result.code == CODE
    assert result.destination_url == DESTINATION
    assert result.enabled is True
    cache_mock.get_destination_url.assert_called_once_with(CODE)


@mock.patch(
    "urlshorten.app.shorten.service.GetShortenedUrlRepository.run",
    new_callable=mock.AsyncMock,
)
@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_retrieve_from_database(cache_mock, db_mock):
    CODE, DESTINATION, ENABLED = "FAKECODE", "https://google.com", True
    cache_mock.get_destination_url.return_value = "", None
    db_mock.return_value = ShortenedUrl(
        code=CODE, destination_url=DESTINATION, enabled=ENABLED
    )

    result = await shorten.retrieve(CODE)
    assert result.code == CODE
    assert result.destination_url == DESTINATION
    assert result.enabled is True
    cache_mock.set_destination_url.assert_called_once_with(CODE, DESTINATION, ENABLED)


@mock.patch(
    "urlshorten.app.shorten.service.GetShortenedUrlRepository.run",
    new_callable=mock.AsyncMock,
)
@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_retrieve_not_found(cache_mock, db_mock):
    CODE = "FAKECODE"
    cache_mock.get_destination_url.return_value = "", None
    db_mock.return_value = None

    result = await shorten.retrieve(CODE)
    assert result is None

    db_mock.assert_called_once_with(code=CODE)
    cache_mock.get_destination_url.assert_called_once_with(CODE)
    cache_mock.set_destination_url.assert_not_called()
