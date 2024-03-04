from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient
from planner.main import app
from planner.users.dependencies import get_user_manager
from planner.users.models import User, UserRead

DB_USER = User(email="user@example.com")
user_manager_mock = AsyncMock()
user_manager_mock.create = AsyncMock(return_value=DB_USER)
app.dependency_overrides[get_user_manager] = lambda: user_manager_mock


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    expected_user = UserRead.model_validate(DB_USER)
    response = await client.post(
        "/users/",
        content=DB_USER.model_dump_json(exclude_unset=True),
    )
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert expected_user == actual_user
