import pytest_asyncio
from planner.core.models import BaseModel
from planner.database import async_engine
from planner.database import async_session as session


@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await async_engine.dispose()
