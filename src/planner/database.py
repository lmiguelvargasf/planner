from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from .config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL.unicode_string(),
    echo=True,
)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Obtain an asynchronous session for the database.

    Returns:
        An asynchronous generator yielding an `AsyncSession` instance.

    """
    async with async_session() as session:
        yield session
