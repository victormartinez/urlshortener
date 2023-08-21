from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from urlshorten.db.session import get_session


router = APIRouter(tags=["urls"])


@router.get("/{code}", status_code=HTTPStatus.OK)
async def resolve_url_code(
    code: str, session: AsyncSession = Depends(get_session)
) -> None:
    return None
