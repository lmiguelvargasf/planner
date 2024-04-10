from typing import Callable
from unittest.mock import AsyncMock

from fastapi import status
from httpx import AsyncClient
from planner.main import app
from planner.users.dependencies import get_user_manager
from planner.users.models import User, UserCreate, UserRead, UserUpdate

USER_CREATE = UserCreate(email="user@example.com")
USER = User.model_validate(USER_CREATE)
USER_UPDATE = UserUpdate(email="updated@example.com")
UPDATED_USER = User.model_validate(
    USER.model_dump() | USER_UPDATE.model_dump(exclude_unset=True)
)


def get_user_manager_mock() -> Callable[[], AsyncMock]:
    user_manager_mock = AsyncMock()
    user_manager_mock.create = AsyncMock(return_value=USER)
    user_manager_mock.get_by_uuid = AsyncMock(return_value=USER)
    user_manager_mock.get_by_email = AsyncMock(return_value=USER)
    user_manager_mock.patch = AsyncMock(return_value=UPDATED_USER)

    return lambda: user_manager_mock


app.dependency_overrides[get_user_manager] = get_user_manager_mock()


async def test_create_user(client: AsyncClient):
    response = await client.post(
        app.url_path_for("create_user"),
        content=USER_CREATE.model_dump_json(exclude_unset=True),
    )
    expected_user = UserRead.model_validate(USER)
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert expected_user == actual_user


async def test_get_user_by_uuid(client: AsyncClient):
    response = await client.get(
        app.url_path_for("read_user_by_uuid", user_uuid=USER.uuid)
    )
    expected_user = UserRead.model_validate(USER)
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert expected_user == actual_user


async def test_get_user_by_email(client: AsyncClient):
    response = await client.get(
        app.url_path_for("read_user_by_email", email=USER.email)
    )
    expected_user = UserRead.model_validate(USER)
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert expected_user == actual_user


async def test_patch_user(client: AsyncClient):
    response = await client.patch(
        app.url_path_for("patch_user", user_uuid=USER.uuid),
        content=USER_UPDATE.model_dump_json(exclude_unset=True),
    )
    expected_user = UserRead.model_validate(UPDATED_USER)
    actual_user = UserRead.model_validate(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert expected_user == actual_user


async def test_delete_user(client: AsyncClient):
    response = await client.delete(app.url_path_for("delete_user", user_uuid=USER.uuid))

    assert response.status_code == status.HTTP_204_NO_CONTENT
