from typing import Optional

from sqlalchemy import select, update

from urlshorten.db.base_repository import BaseRepository
from urlshorten.db.models import DBShortenedUrl  # type: ignore[attr-defined]

from .entities import ShortenedUrl


class PersistShortenedUrlRepository(BaseRepository):
    async def execute(self, code: str, destination_url: str) -> None:
        db_object = DBShortenedUrl(code=code, destination_url=destination_url)
        self.db_session.add(db_object)
        await self.db_session.commit()


class GetShortenedUrlRepository(BaseRepository):
    async def execute(self, code: str) -> Optional[ShortenedUrl]:
        query = select(DBShortenedUrl.destination_url, DBShortenedUrl.enabled).where(
            DBShortenedUrl.code == code
        )
        result = await self.db_session.execute(query)
        db_object = result.first()
        if not db_object:
            return None
        # gently reminder: db_object is a tuple
        destination_url, enabled = db_object[0], db_object[1]
        return ShortenedUrl(
            code=code,
            destination_url=destination_url,
            enabled=enabled,
        )


class UpdateShortenedUrlRepository(BaseRepository):
    async def execute(
        self,
        code: str,
        *,
        destination_url: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> int:
        if destination_url is None and enabled is None:
            return 0

        query_update = update(DBShortenedUrl).where(DBShortenedUrl.code == code)
        if destination_url:
            query_update = query_update.values(destination_url=destination_url)

        if enabled is not None:
            query_update = query_update.values(enabled=enabled)

        result = await self.db_session.execute(query_update)
        await self.db_session.commit()
        return result.rowcount  # type: ignore
