from pydantic import EmailStr
from sqlmodel import Column, Field, String

from ..core.models import BaseModel


class User(BaseModel, table=True):
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )
    hashed_password: str | None
    first_name: str | None = Field(nullable=True)
    last_name: str | None = Field(nullable=True)
    is_active: bool = Field(
        default=True, nullable=False, sa_column_kwargs=dict(server_default="TRUE")
    )
    is_superuser: bool = Field(
        default=False, nullable=False, sa_column_kwargs=dict(server_default="FALSE")
    )
