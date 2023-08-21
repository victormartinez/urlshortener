from abc import abstractmethod
from typing import Any

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from urlshorten.app.exceptions import AppException, AppExceptionType


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def run(self, *args: Any, **kwargs: Any):  # type: ignore
        try:
            return await self.execute(*args, **kwargs)
        except IntegrityError:
            raise AppException(
                type=AppExceptionType.DATABASE_INTEGRITY_ERROR,
                message="Integrity error regarding data.",
            )
        except SQLAlchemyError as exc:
            raise AppException(
                type=AppExceptionType.DATABASE_ERROR, message=str(exc)
            )

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
        pass
