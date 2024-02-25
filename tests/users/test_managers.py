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
async def db_basic_user(session: AsyncSession, validated_basic_user):
    manager = UserManager(session)
    db_user = await manager.create(validated_basic_user)
    return db_user


@pytest_asyncio.fixture
async def db_complete_user(session: AsyncSession, validated_complete_user):
    manager = UserManager(session)
    db_user = await manager.create(validated_complete_user)
    return db_user


@pytest.mark.asyncio
async def test_user_creation_required_fields(db_basic_user, validated_basic_user):
    assert db_basic_user.uuid == validated_basic_user.uuid
    assert db_basic_user.first_name is None
    assert db_basic_user.middle_name is None
    assert db_basic_user.last_name is None
    assert db_basic_user.second_last_name is None
    assert db_basic_user.date_of_birth is None
    assert db_basic_user.sex is None
    assert db_basic_user.email == validated_basic_user.email
    assert db_basic_user.hashed_password is None
    assert db_basic_user.is_active is True
    assert db_basic_user.is_superuser is False
    assert db_basic_user.created_at == validated_basic_user.created_at
    assert db_basic_user.updated_at == validated_basic_user.updated_at


@pytest.mark.asyncio
async def test_user_creation_full_data(db_complete_user, validated_complete_user):
    assert db_complete_user.uuid == validated_complete_user.uuid
    assert db_complete_user.first_name == validated_complete_user.first_name
    assert db_complete_user.middle_name == validated_complete_user.middle_name
    assert db_complete_user.last_name == validated_complete_user.last_name
    assert db_complete_user.second_last_name == validated_complete_user.second_last_name
    assert db_complete_user.date_of_birth == validated_complete_user.date_of_birth
    assert db_complete_user.sex == validated_complete_user.sex
    assert db_complete_user.email == validated_complete_user.email
    assert db_complete_user.hashed_password == validated_complete_user.hashed_password
    assert db_complete_user.is_active == validated_complete_user.is_active
    assert db_complete_user.is_superuser == validated_complete_user.is_superuser
    assert db_complete_user.created_at == validated_complete_user.created_at
    assert db_complete_user.updated_at == validated_complete_user.updated_at


@pytest.mark.asyncio
async def test_create_user_with_unique_email(session: AsyncSession, db_basic_user):
    # create another user with same email
    another_user = UserCreate(email=EMAIL)
    validated_user = User.model_validate(another_user)
    manager = UserManager(session)

    with pytest.raises(IntegrityError, match="unique constraint"):
        await manager.create(validated_user)


@pytest.mark.asyncio
async def test_get_user_by_uuid(session: AsyncSession, db_basic_user):
    manager = UserManager(session)
    user = await manager.get_by_uuid(uuid=db_basic_user.uuid)
    assert user == db_basic_user


@pytest.mark.asyncio
async def test_get_user_by_uuid_not_found(session: AsyncSession):
    manager = UserManager(session)
    uuid = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(NoResultFound, match="No row was found"):
        await manager.get_by_uuid(uuid=uuid)


@pytest.mark.asyncio
async def test_get_user_by_email(session: AsyncSession, db_basic_user):
    manager = UserManager(session)
    user = await manager.get_by_email(email=EMAIL)
    assert user == db_basic_user


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(session: AsyncSession):
    manager = UserManager(session)

    with pytest.raises(NoResultFound, match="No row was found"):
        await manager.get_by_email(email=EMAIL)


@pytest.mark.asyncio
async def test_patch_user(session: AsyncSession, db_basic_user):
    manager = UserManager(session)
    user = UserUpdate(first_name=FIRST_NAME, last_name=LAST_NAME)

    updated_user = await manager.patch(uuid=db_basic_user.uuid, user=user)

    assert updated_user.uuid == db_basic_user.uuid
    assert updated_user.first_name == FIRST_NAME
    assert updated_user.last_name == LAST_NAME


@pytest.mark.asyncio
async def test_patch_email_is_none(session: AsyncSession, db_basic_user):
    manager = UserManager(session)
    user = UserUpdate(email=None)

    with pytest.raises(IntegrityError, match="violates not-null constraint"):
        await manager.patch(uuid=db_basic_user.uuid, user=user)


@pytest.mark.asyncio
async def test_patch_user_with_unique_email(session: AsyncSession, db_basic_user):
    manager = UserManager(session)

    # create another user
    another_email = "another@example.com"  # noqa: N806
    user = UserCreate(email=another_email)
    validated_user = User.model_validate(user)
    await manager.create(validated_user)

    # update user with email of another user
    user = UserUpdate(email=another_email)

    with pytest.raises(IntegrityError, match="unique constraint"):
        await manager.patch(uuid=db_basic_user.uuid, user=user)


@pytest.mark.asyncio
async def test_patch_user_not_found(session: AsyncSession):
    manager = UserManager(session)
    user = UserUpdate(first_name=FIRST_NAME, last_name=LAST_NAME)
    uuid = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(NoResultFound, match="No row was found"):
        await manager.patch(uuid=uuid, user=user)


@pytest.mark.asyncio
async def test_delete_user(session: AsyncSession, db_basic_user):
    manager = UserManager(session)
    await manager.delete(uuid=db_basic_user.uuid)

    with pytest.raises(NoResultFound, match="No row was found"):
        await manager.get_by_uuid(uuid=db_basic_user.uuid)


@pytest.mark.asyncio
async def test_delete_user_not_found(session: AsyncSession):
    manager = UserManager(session)
    uuid = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(NoResultFound, match="No row was found"):
        await manager.delete(uuid=uuid)
