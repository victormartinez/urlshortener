from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from infrastructure import logging
from urlshorten.api.urls.schema import (
    CodeUrlOut,
    DestinationUrlIn,
    DestinationUrlOut,
    UpdateDestinationUrlIn,
)
from urlshorten.app import shorten
from urlshorten.app.exceptions import AppException, AppExceptionType
from urlshorten.db.session import get_session

router = APIRouter(tags=["urls"])
logger = logging.get_logger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=CodeUrlOut)
async def create(
    payload: DestinationUrlIn, session: AsyncSession = Depends(get_session)
) -> CodeUrlOut:
    for attempt_number in range(settings.URL_CODE_COLLISION_ATTEMPTS):
        try:
            code = await shorten.create(session, payload.destination_url)
            return CodeUrlOut(code=code)
        except AppException:
            logger.exception(
                "error shortening url",
                destination_url=payload.destination_url,
                attempt=attempt_number,
            )

    raise AppException(
        type=AppExceptionType.INTEGRITY_ERROR,
        message="It was not possible to generate a code for the destination url.",
    )


@router.get("/{code}")
async def resolve_url_code(code: str, redirect: Optional[bool] = True):
    shortened_url_object = await shorten.retrieve(code)
    if not shortened_url_object:
        raise AppException(
            type=AppExceptionType.ENTITY_NOT_FOUND, message="URL not found"
        )
    if not shortened_url_object.enabled:
        raise AppException(
            type=AppExceptionType.DISABLED_RESOURCE,
            message="The related URL is disabled.",
        )

    if redirect is True:
        return RedirectResponse(url=shortened_url_object.destination_url)
    return DestinationUrlOut(destination_url=shortened_url_object.destination_url)


@router.patch("/{code}", status_code=HTTPStatus.OK)
async def update_destination_url(
    code: str,
    payload: UpdateDestinationUrlIn,
    session: AsyncSession = Depends(get_session),
) -> None:
    updated = await shorten.update(
        session, code, destination_url=payload.destination_url, enabled=payload.enabled
    )
    if not updated:
        raise AppException(
            type=AppExceptionType.ENTITY_NOT_FOUND,
            message="URL not found.",
        )
