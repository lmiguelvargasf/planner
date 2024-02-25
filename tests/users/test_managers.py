import pytest
from planner.users.managers import UserManager
from planner.users.models import Sex, User, UserCreate
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_user_creation_required_fields(session: AsyncSession):
    manager = UserManager(session)
    user = UserCreate(email="user@example.com")
    validated_user = User.model_validate(user)
    db_user = await manager.create(validated_user)

    assert db_user.uuid == validated_user.uuid
    assert db_user.first_name is None
    assert db_user.middle_name is None
    assert db_user.last_name is None
    assert db_user.second_last_name is None
    assert db_user.date_of_birth is None
    assert db_user.sex is None
    assert db_user.email == validated_user.email
    assert db_user.hashed_password is None
    assert db_user.is_active is True
    assert db_user.is_superuser is False
    assert db_user.created_at == validated_user.created_at
    assert db_user.updated_at == validated_user.updated_at


@pytest.mark.asyncio
async def test_user_creation_full_data(session: AsyncSession):
    manager = UserManager(session)
    user = UserCreate(
        first_name="John",
        middle_name="Doe",
        last_name="Smith",
        second_last_name="Johnson",
        date_of_birth="1990-01-01",
        sex=Sex.MALE,
        email="user@example.com",
        hashed_password=("password"),
        is_active=False,
        is_superuser=True,
    )
    validated_user = User.model_validate(user)
    db_user = await manager.create(validated_user)

    assert db_user.uuid == validated_user.uuid
    assert db_user.first_name == validated_user.first_name
    assert db_user.middle_name == validated_user.middle_name
    assert db_user.last_name == validated_user.last_name
    assert db_user.second_last_name == validated_user.second_last_name
    assert db_user.date_of_birth == validated_user.date_of_birth
    assert db_user.sex == validated_user.sex
    assert db_user.email == validated_user.email
    assert db_user.hashed_password == validated_user.hashed_password
    assert db_user.is_active == validated_user.is_active
    assert db_user.is_superuser == validated_user.is_superuser
    assert db_user.created_at == validated_user.created_at
    assert db_user.updated_at == validated_user.updated_at
