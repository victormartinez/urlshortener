from unittest import mock

import pytest

from urlshorten.app import shorten


@mock.patch(
    "urlshorten.app.shorten.service.PersistShortenedUrlRepository.run",
    new_callable=mock.AsyncMock,
)
@mock.patch("urlshorten.app.shorten.service.cache", new_callable=mock.AsyncMock)
@pytest.mark.asyncio
async def test_create(cache_mock, run_mock):
    SESSION, DESTINATION = mock.AsyncMock(), "https://google.com"
    await shorten.create(SESSION, DESTINATION)

    generated_code = run_mock.call_args_list[0].kwargs["code"]
    run_mock.assert_called_once_with(code=generated_code, destination_url=DESTINATION)
    cache_mock.set_destination_url.assert_called_once_with(generated_code, DESTINATION)
