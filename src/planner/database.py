from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL.unicode_string(),
    echo=True,
)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def inject_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.

    Designed first for FastAPI's `Depends` to facilitate dependency injection,
    it should be suitable and functional in other asynchronous contexts.

    Yields:
        An async database session.
    """
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a context manager for async database sessions.

    Yields:
        An async database session.
    """
    async with async_session() as session:
        yield session
