from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from .config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL.unicode_string(),
    echo=True,
)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def inject_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for asynchronous web applications, designed for
    seamless integration with dependency injection systems. This function is
    crafted for use with FastAPI's `Depends`, but it should also work well
    with other async frameworks.

    Yields:
        An async database session.
    """
    async with async_session() as session:
        yield session
