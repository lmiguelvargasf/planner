from datetime import date
from enum import StrEnum, auto

from pydantic import EmailStr
from sqlmodel import AutoString, Field, SQLModel, false, true

from ..core.models import BaseModel


class Sex(StrEnum):
    """Enum to represent human biological sexes."""

    MALE = auto()
    FEMALE = auto()


class User(BaseModel, table=True):
    """Model representing a user."""

    first_name: str | None = Field(nullable=True, default=None)
    middle_name: str | None = Field(nullable=True, default=None)
    last_name: str | None = Field(nullable=True, default=None)
    second_last_name: str | None = Field(nullable=True, default=None)
    date_of_birth: date | None = Field(nullable=True, default=None)
    sex: Sex | None = Field(nullable=True, default=None)
    email: EmailStr = Field(sa_type=AutoString, unique=True, nullable=False)
    hashed_password: str | None = Field(nullable=True, default=None)
    is_active: bool = Field(
        default=True, nullable=False, sa_column_kwargs=dict(server_default=true())
    )
    is_superuser: bool = Field(
        default=False, nullable=False, sa_column_kwargs=dict(server_default=false())
    )


class BaseUser(SQLModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    second_last_name: str | None = None
    date_of_birth: date | None = None
    sex: Sex | None = None
    hashed_password: str | None = None


class UserCreate(BaseUser):
    """Model representing a user to be created."""

    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseUser):
    """Model representing a user to be updated."""

    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
