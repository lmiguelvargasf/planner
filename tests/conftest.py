import pytest_asyncio
from planner.core.models import BaseModel
from planner.database import async_engine, async_session


@pytest_asyncio.fixture(scope="function")
async def session():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with async_session() as async_db_session:
        yield async_db_session

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await async_engine.dispose()
