from datetime import datetime

import pytest
import pytest_asyncio
from planner.users.exceptions import UserError, UserErrorMessage
from planner.users.managers import UserManager
from planner.users.models import Sex, User, UserCreate, UserUpdate
from sqlmodel.ext.asyncio.session import AsyncSession

EMAIL = "user@example.com"
FIRST_NAME = "John"
LAST_NAME = "Smith"
UUID_NOT_IN_DB = "00000000-0000-0000-0000-000000000000"
BASIC_USER_CREATE = UserCreate(email=EMAIL)
USER_DATA = dict(
    first_name=FIRST_NAME,
    middle_name="Doe",
    last_name=LAST_NAME,
    second_last_name="Johnson",
    date_of_birth=datetime.strptime("1990-01-01", "%Y-%m-%d").date(),
    sex=Sex.MALE,
    email=EMAIL,
    hashed_password="password",
    is_active=False,
    is_superuser=True,
)
COMPLETE_USER_CREATE = UserCreate(**USER_DATA)
pytestmark = pytest.mark.asyncio


@pytest.fixture
def user_manager(session: AsyncSession):
    manager = UserManager(session)
    return manager


@pytest_asyncio.fixture
async def db_basic_user(user_manager):
    db_user = await user_manager.create(BASIC_USER_CREATE)
    return db_user


@pytest_asyncio.fixture
async def db_complete_user(user_manager):
    db_user = await user_manager.create(COMPLETE_USER_CREATE)
    return db_user


async def test_user_creation_required_fields(user_manager):
    initial_count = await user_manager.count
    db_user = await user_manager.create(BASIC_USER_CREATE)
    assert db_user.email == EMAIL
    final_count = await user_manager.count
    assert final_count == initial_count + 1


async def test_user_creation_full_data(user_manager):
    initial_count = await user_manager.count
    db_user = await user_manager.create(COMPLETE_USER_CREATE)
    for key, value in USER_DATA.items():
        assert getattr(db_user, key) == value
    final_count = await user_manager.count
    assert final_count == initial_count + 1


async def test_create_user_with_unique_email(db_basic_user, user_manager):
    initial_count = await user_manager.count
    with pytest.raises(UserError, match=UserErrorMessage.DUPLICATE_EMAIL):
        await user_manager.create(BASIC_USER_CREATE)
    await user_manager.session.rollback()
    final_count = await user_manager.count
    assert final_count == initial_count


async def test_get_user_by_uuid(user_manager, db_basic_user):
    user = await user_manager.get_by_uuid(uuid=db_basic_user.uuid)
    assert user == db_basic_user


async def test_get_user_by_uuid_not_found(user_manager):
    with pytest.raises(UserError, match=UserErrorMessage.NOT_FOUND_BY_UUID):
        await user_manager.get_by_uuid(uuid=UUID_NOT_IN_DB)


async def test_get_user_by_email(user_manager, db_basic_user):
    user = await user_manager.get_by_email(email=EMAIL)
    assert user == db_basic_user


async def test_get_user_by_email_not_found(user_manager):
    with pytest.raises(UserError, match=UserErrorMessage.NOT_FOUND_BY_EMAIL):
        await user_manager.get_by_email(email=EMAIL)


async def test_patch_user(user_manager, db_complete_user: User):
    user_before_update = db_complete_user.model_copy()
    new_data = dict(first_name="Sam", last_name="Johnson")
    user = UserUpdate(**new_data)
    user_data = USER_DATA | new_data

    updated_user = await user_manager.patch(uuid=db_complete_user.uuid, user=user)

    for key, value in user_data.items():
        assert getattr(updated_user, key) == value

    assert updated_user.uuid == user_before_update.uuid
    assert updated_user.created_at == user_before_update.created_at
    assert updated_user.updated_at > user_before_update.updated_at


async def test_patch_email_is_none(user_manager, db_basic_user):
    user = UserUpdate(email=None)

    with pytest.raises(UserError, match=UserErrorMessage.EMAIL_REQUIRED):
        await user_manager.patch(uuid=db_basic_user.uuid, user=user)


async def test_patch_user_with_unique_email(user_manager, db_basic_user):
    # create another user
    another_email = "another@example.com"
    user = UserCreate(email=another_email)
    validated_user = User.model_validate(user)
    await user_manager.create(validated_user)

    # update user with email of another user
    user = UserUpdate(email=another_email)

    with pytest.raises(UserError, match=UserErrorMessage.DUPLICATE_EMAIL):
        await user_manager.patch(uuid=db_basic_user.uuid, user=user)


async def test_patch_user_not_found(user_manager):
    user = UserUpdate(first_name=FIRST_NAME, last_name=LAST_NAME)

    with pytest.raises(UserError, match=UserErrorMessage.NOT_FOUND_BY_UUID):
        await user_manager.patch(uuid=UUID_NOT_IN_DB, user=user)


async def test_delete_user(db_basic_user, user_manager):
    initial_count = await user_manager.count
    await user_manager.delete(uuid=db_basic_user.uuid)

    with pytest.raises(UserError, match=UserErrorMessage.NOT_FOUND_BY_UUID):
        await user_manager.get_by_uuid(uuid=db_basic_user.uuid)

    final_count = await user_manager.count
    assert final_count == initial_count - 1


async def test_delete_user_not_found(user_manager):
    with pytest.raises(UserError, match=UserErrorMessage.NOT_FOUND_BY_UUID):
        await user_manager.delete(uuid=UUID_NOT_IN_DB)
