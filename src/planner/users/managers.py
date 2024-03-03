from dataclasses import dataclass
from uuid import UUID

from asyncpg.exceptions import NotNullViolationError, UniqueViolationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .exceptions import UserError, UserErrorMessage
from .models import User, UserCreate, UserUpdate


@dataclass(repr=False, eq=False)
class UserManager:
    session: AsyncSession

    async def create(self, user: UserCreate) -> User:
        db_user = User.model_validate(user)
        await self._save_and_refresh(db_user)
        return db_user

    async def get_by_uuid(self, *, uuid: UUID) -> User:
        try:
            db_user = await self.session.get_one(User, uuid)
        except NoResultFound as error:
            raise UserError(message=UserErrorMessage.NOT_FOUND_BY_UUID) from error

        return db_user

    async def get_by_email(self, *, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.exec(query)
        try:
            db_user = result.one()
        except NoResultFound as error:
            raise UserError(message=UserErrorMessage.NOT_FOUND_BY_EMAIL) from error
        return db_user

    async def patch(self, *, uuid: UUID, user: UserUpdate) -> User:
        db_user = await self.get_by_uuid(uuid=uuid)
        dumped_user = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(dumped_user)
        await self._save_and_refresh(db_user)
        return db_user

    async def delete(self, *, uuid: UUID) -> None:
        db_user = await self.get_by_uuid(uuid=uuid)
        await self.session.delete(db_user)
        await self.session.commit()

    def _handle_integrity_error(self, error: IntegrityError) -> None:
        match error.orig.sqlstate:
            case NotNullViolationError.sqlstate:
                raise UserError(message=UserErrorMessage.EMAIL_REQUIRED) from error
            case UniqueViolationError.sqlstate:
                raise UserError(message=UserErrorMessage.DUPLICATE_EMAIL) from error
            case _:
                raise error from error

    async def _save_and_refresh(self, user: User) -> None:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as error:
            self._handle_integrity_error(error)
        await self.session.refresh(user)
