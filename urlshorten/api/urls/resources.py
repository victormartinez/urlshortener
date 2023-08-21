from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from urlshorten.api.urls.schema import (
    CodeUrlOut,
    DestinationUrlIn,
    UpdateDestinationUrlIn,
)
from urlshorten.app import shorten
from urlshorten.app.exceptions import AppException, AppExceptionType
from urlshorten.db.session import get_session

router = APIRouter(tags=["urls"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=CodeUrlOut)
async def create(
    payload: DestinationUrlIn, session: AsyncSession = Depends(get_session)
) -> CodeUrlOut:
    code = await shorten.create(session, payload.destination_url)
    return CodeUrlOut(code=code)


@router.get(
    "/{code}",
    status_code=HTTPStatus.PERMANENT_REDIRECT,
    response_model=RedirectResponse,
)
async def resolve_url_code(code: str) -> RedirectResponse:
    shortened_url_object = await shorten.retrieve(code)
    if shortened_url_object.enabled:
        return RedirectResponse(url=shortened_url_object.destination_url)
    raise AppException(
        type=AppExceptionType.DISABLED_RESOURCE, message="The related URL is disabled."
    )


@router.patch("/{code}", status_code=HTTPStatus.OK)
async def update_destination_url(
    code: str,
    payload: UpdateDestinationUrlIn,
    session: AsyncSession = Depends(get_session),
) -> None:
    await shorten.update(session, code, payload.destination_url, payload.enabled)
