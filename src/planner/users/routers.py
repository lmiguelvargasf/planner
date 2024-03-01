from uuid import UUID

from fastapi import APIRouter, Depends, status

from .dependencies import get_user_manager
from .managers import UserManager
from .models import User, UserCreate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_user(
    user: UserCreate, user_manager: UserManager = Depends(get_user_manager)
) -> UserRead:
    validated_user = User.model_validate(user)
    db_user = await user_manager.create(validated_user)
    return db_user


@router.get(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def read_user_by_uuid(
    user_uuid: UUID, user_manager: UserManager = Depends(get_user_manager)
) -> UserRead:
    db_user = await user_manager.get_by_uuid(uuid=user_uuid)
    return db_user


@router.get(
    "/email/{email}",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def read_user_by_email(
    email: str, user_manager: UserManager = Depends(get_user_manager)
) -> UserRead:
    db_user = await user_manager.get_by_email(email=email)
    return db_user
