import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from planner.core.models import BaseModel
from planner.database import async_engine, async_session
from planner.main import app


@pytest_asyncio.fixture(scope="function")
async def session():
    """
    Create and tear down an asyncrhonous database session.

    First, it establishes a connection to the database and creates all tables
    defined in the BaseModel's metadata. Second, it yields a session that tests
    can use to interact with the database. Finally, once a test completes, it
    drops all tables from the database and disposes the engine.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with async_session() as async_db_session:
        yield async_db_session

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
