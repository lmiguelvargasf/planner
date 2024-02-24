from dataclasses import dataclass
from uuid import UUID

from sqlmodel import select
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

    async def get_by_uuid(self, *, uuid: UUID) -> User | None:
        return await self.session.get(User, uuid)

    async def update(self, *, uuid: UUID, user: User) -> User:
        db_user = await self._get_by_uuid(uuid)
        dumped_user = db_user.model_dump() | user.model_dump()
        db_user.sqlmodel_update(dumped_user)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def _get_by_uuid(self, uuid: UUID) -> User:
        query = select(User).where(User.uuid == uuid)
        result = await self.session.exec(query)
        db_user = result.one()
        return db_user
