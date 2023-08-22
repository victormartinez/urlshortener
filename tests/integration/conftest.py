import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from settings import build_database_uri, build_engine_config, build_session_config
from urlshorten.db.models import DBShortenedUrl
from urlshorten.db.session import SessionLocal
from urlshorten.main import app

engine = create_async_engine(build_database_uri(), **build_engine_config())
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, **build_session_config()
)


@pytest_asyncio.fixture(scope="function")
async def session(override_async_session):
    app.dependency_overrides[SessionLocal] = override_async_session

    yield override_async_session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db(session):
    await session.execute(delete(DBShortenedUrl))
    await session.commit()


@pytest_asyncio.fixture()
async def override_async_session():
    session = TestingSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
