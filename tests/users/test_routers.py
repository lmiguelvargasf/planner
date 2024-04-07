from unittest.mock import AsyncMock

from fastapi import status
from httpx import AsyncClient
from planner.main import app
from planner.users.dependencies import get_user_manager
from planner.users.models import User, UserRead

DB_USER = User(email="user@example.com")
user_manager_mock = AsyncMock()
validated_user = User.model_validate(DB_USER)
user_manager_mock.create = AsyncMock(return_value=validated_user)
user_manager_mock.get_by_uuid = AsyncMock(return_value=validated_user)
app.dependency_overrides[get_user_manager] = lambda: user_manager_mock


async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users/",
        content=DB_USER.model_dump_json(exclude_unset=True),
    )
    expected_user = UserRead.model_validate(DB_USER)
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert expected_user == actual_user


async def test_get_user_by_uuid(client: AsyncClient):
    response = await client.get(f"/users/{DB_USER.uuid}")
    expected_user = UserRead.model_validate(DB_USER)
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert expected_user == actual_user
