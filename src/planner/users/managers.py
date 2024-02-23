from dataclasses import dataclass

from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User


@dataclass(repr=False, eq=False)
class UserManager:
    session: AsyncSession

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
