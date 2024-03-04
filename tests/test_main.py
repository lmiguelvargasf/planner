import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_app_status(client: AsyncClient):
    response = await client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "up"}
