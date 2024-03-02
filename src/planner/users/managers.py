from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .exceptions import UserError, UserErrorMessage
from .models import User, UserUpdate


@dataclass(repr=False, eq=False)
class UserManager:
    session: AsyncSession

    async def create(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as error:
            raise UserError(message=UserErrorMessage.DUPLICATE_EMAIL.value) from error

        await self.session.refresh(user)
        return user

    async def get_by_uuid(self, *, uuid: UUID) -> User:
        return await self.session.get_one(User, uuid)

    async def get_by_email(self, *, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.exec(query)
        db_user = result.one()
        return db_user

    async def patch(self, *, uuid: UUID, user: UserUpdate) -> User:
        db_user = await self.get_by_uuid(uuid=uuid)
        dumped_user = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(dumped_user)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete(self, *, uuid: UUID) -> None:
        db_user = await self.get_by_uuid(uuid=uuid)
        await self.session.delete(db_user)
        await self.session.commit()
