from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import inject_db_session
from .managers import UserManager


async def get_user_manager(
    session: AsyncSession = Depends(inject_db_session),
) -> UserManager:
    return UserManager(session=session)
