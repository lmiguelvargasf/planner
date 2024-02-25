import pytest
import pytest_asyncio
from planner.users.managers import UserManager
from planner.users.models import Sex, User, UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel.ext.asyncio.session import AsyncSession

EMAIL = "user@example.com"
FIRST_NAME = "John"
LAST_NAME = "Smith"


@pytest.fixture
def user_manager(session: AsyncSession):
    manager = UserManager(session)
    return manager


@pytest.fixture
def validated_basic_user():
    user = UserCreate(email=EMAIL)
    validated_user = User.model_validate(user)
    return validated_user


@pytest.fixture
def validated_complete_user():
    user = UserCreate(
        first_name=FIRST_NAME,
        middle_name="Doe",
        last_name=LAST_NAME,
        second_last_name="Johnson",
        date_of_birth="1990-01-01",
        sex=Sex.MALE,
        email=EMAIL,
        hashed_password=("password"),
        is_active=False,
        is_superuser=True,
    )
    validated_user = User.model_validate(user)
    return validated_user


@pytest_asyncio.fixture
async def db_basic_user(validated_basic_user, user_manager):
    db_user = await user_manager.create(validated_basic_user)
    return db_user


@pytest_asyncio.fixture
async def db_complete_user(validated_complete_user, user_manager):
    db_user = await user_manager.create(validated_complete_user)
    return db_user


@pytest.mark.asyncio
async def test_user_creation_required_fields(db_basic_user, validated_basic_user):
    assert db_basic_user == validated_basic_user


@pytest.mark.asyncio
async def test_user_creation_full_data(db_complete_user, validated_complete_user):
    assert db_complete_user == validated_complete_user


@pytest.mark.asyncio
async def test_create_user_with_unique_email(db_basic_user, user_manager):
    # create another user with same email
    user = UserCreate(email=EMAIL)
    validated_user = User.model_validate(user)

    with pytest.raises(IntegrityError, match="unique constraint"):
        await user_manager.create(validated_user)


@pytest.mark.asyncio
async def test_get_user_by_uuid(user_manager, db_basic_user):
    user = await user_manager.get_by_uuid(uuid=db_basic_user.uuid)
    assert user == db_basic_user


@pytest.mark.asyncio
async def test_get_user_by_uuid_not_found(user_manager):
    uuid = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(NoResultFound, match="No row was found"):
        await user_manager.get_by_uuid(uuid=uuid)


@pytest.mark.asyncio
async def test_get_user_by_email(user_manager, db_basic_user):
    user = await user_manager.get_by_email(email=EMAIL)
    assert user == db_basic_user


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_manager):
    with pytest.raises(NoResultFound, match="No row was found"):
        await user_manager.get_by_email(email=EMAIL)


@pytest.mark.asyncio
async def test_patch_user(user_manager, db_complete_user: User):
    user_before_update = db_complete_user.model_copy()
    user = UserUpdate(first_name="Sam", last_name="Johnson")
    updated_user = await user_manager.patch(uuid=db_complete_user.uuid, user=user)

    assert updated_user.uuid == user_before_update.uuid
    assert updated_user.first_name == "Sam"
    assert updated_user.middle_name == user_before_update.middle_name
    assert updated_user.last_name == "Johnson"
    assert updated_user.second_last_name == user_before_update.second_last_name
    assert updated_user.date_of_birth == user_before_update.date_of_birth
    assert updated_user.sex == user_before_update.sex
    assert updated_user.email == user_before_update.email
    assert updated_user.hashed_password == user_before_update.hashed_password
    assert updated_user.is_active == user_before_update.is_active
    assert updated_user.is_superuser == user_before_update.is_superuser
    assert updated_user.created_at == user_before_update.created_at
    assert updated_user.updated_at > user_before_update.updated_at


@pytest.mark.asyncio
async def test_patch_email_is_none(user_manager, db_basic_user):
    user = UserUpdate(email=None)

    with pytest.raises(IntegrityError, match="violates not-null constraint"):
        await user_manager.patch(uuid=db_basic_user.uuid, user=user)


@pytest.mark.asyncio
async def test_patch_user_with_unique_email(user_manager, db_basic_user):
    # create another user
    another_email = "another@example.com"  # noqa: N806
    user = UserCreate(email=another_email)
    validated_user = User.model_validate(user)
    await user_manager.create(validated_user)

    # update user with email of another user
    user = UserUpdate(email=another_email)

    with pytest.raises(IntegrityError, match="unique constraint"):
        await user_manager.patch(uuid=db_basic_user.uuid, user=user)


@pytest.mark.asyncio
async def test_patch_user_not_found(user_manager):
    user = UserUpdate(first_name=FIRST_NAME, last_name=LAST_NAME)
    uuid = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(NoResultFound, match="No row was found"):
        await user_manager.patch(uuid=uuid, user=user)


@pytest.mark.asyncio
async def test_delete_user(db_basic_user, user_manager):
    await user_manager.delete(uuid=db_basic_user.uuid)

    with pytest.raises(NoResultFound, match="No row was found"):
        await user_manager.get_by_uuid(uuid=db_basic_user.uuid)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_manager):
    uuid = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(NoResultFound, match="No row was found"):
        await user_manager.delete(uuid=uuid)
