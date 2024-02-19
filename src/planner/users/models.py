from datetime import date
from enum import StrEnum, auto

from pydantic import EmailStr
from sqlalchemy import false, true
from sqlmodel import Column, Field, String

from ..core.models import BaseModel


class Sex(StrEnum):
    MALE = auto()
    FEMALE = auto()


class User(BaseModel, table=True):
    first_name: str | None = Field(nullable=True)
    middle_name: str | None = Field(nullable=True)
    last_name: str | None = Field(nullable=True)
    second_last_name: str | None = Field(nullable=True)
    date_of_birth: date | None = Field(nullable=True)
    sex: Sex | None = Field(nullable=True)
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )
    hashed_password: str | None
    is_active: bool = Field(
        default=True, nullable=False, sa_column_kwargs=dict(server_default=true())
    )
    is_superuser: bool = Field(
        default=False, nullable=False, sa_column_kwargs=dict(server_default=false())
    )
