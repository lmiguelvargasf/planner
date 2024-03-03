from uuid import UUID

from fastapi import APIRouter, Depends, status

from .dependencies import get_user_manager
from .managers import UserManager
from .models import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate, user_manager: UserManager = Depends(get_user_manager)
) -> UserRead:
    db_user = await user_manager.create(user)
    return db_user


@router.get(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
)
async def read_user_by_uuid(
    user_uuid: UUID, user_manager: UserManager = Depends(get_user_manager)
) -> UserRead:
    db_user = await user_manager.get_by_uuid(uuid=user_uuid)
    return db_user


@router.get(
    "/email/{email}",
    status_code=status.HTTP_200_OK,
)
async def read_user_by_email(
    email: str, user_manager: UserManager = Depends(get_user_manager)
) -> UserRead:
    db_user = await user_manager.get_by_email(email=email)
    return db_user


@router.patch(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
)
async def patch_user(
    user_uuid: UUID,
    user: UserUpdate,
    user_manager: UserManager = Depends(get_user_manager),
) -> UserRead:
    db_user = await user_manager.patch(uuid=user_uuid, user=user)
    return db_user


@router.delete(
    "/{user_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_uuid: UUID, user_manager: UserManager = Depends(get_user_manager)
) -> None:
    await user_manager.delete(uuid=user_uuid)
