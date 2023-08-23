from unittest import mock

import pytest

from urlshorten.app import shorten


@mock.patch(
    "urlshorten.app.shorten.service.UpdateShortenedUrlRepository.run",
    new_callable=mock.AsyncMock,
)
@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_update_destination_url(cache_mock, run_mock):
    run_mock.return_value = 1
    SESSION, CODE, DESTINATION = mock.AsyncMock(), "F4K3", "https://google.com"
    updated = await shorten.update(SESSION, CODE, destination_url=DESTINATION)

    assert updated == 1
    generated_code = run_mock.call_args_list[0].args[0]
    run_mock.assert_called_once_with(
        generated_code, destination_url=DESTINATION, enabled=None
    )
    cache_mock.delete_destination_url.assert_called_once_with(generated_code)


@mock.patch(
    "urlshorten.app.shorten.service.UpdateShortenedUrlRepository.run",
    new_callable=mock.AsyncMock,
)
@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_update_destination_url_and_enabled(cache_mock, run_mock):
    run_mock.return_value = 1
    SESSION, CODE, DESTINATION = mock.AsyncMock(), "F4K3", "https://google.com"
    updated = await shorten.update(
        SESSION, CODE, destination_url=DESTINATION, enabled=True
    )

    assert updated == 1
    generated_code = run_mock.call_args_list[0].args[0]
    run_mock.assert_called_once_with(
        generated_code, destination_url=DESTINATION, enabled=True
    )
    cache_mock.delete_destination_url.assert_called_once_with(generated_code)


@mock.patch(
    "urlshorten.app.shorten.service.UpdateShortenedUrlRepository.run",
    new_callable=mock.AsyncMock,
)
@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_update_enabled(cache_mock, run_mock):
    run_mock.return_value = 1
    SESSION, CODE = mock.AsyncMock(), "F4K3"
    updated = await shorten.update(SESSION, CODE, enabled=True)

    assert updated == 1
    generated_code = run_mock.call_args_list[0].args[0]
    run_mock.assert_called_once_with(generated_code, destination_url=None, enabled=True)
    cache_mock.delete_destination_url.assert_called_once_with(generated_code)
