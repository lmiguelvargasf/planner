from abc import ABC
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func
from sqlmodel import TIMESTAMP, Field, SQLModel, text

from .utils import camel_to_snake


class UUIDMixin(SQLModel):
    """Mixin class that adds a unique UUID field."""

    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs=dict(server_default=text("gen_random_uuid()"), unique=True),
    )


class TimeStampedMixin(SQLModel):
    """Mixin class that adds created and modified timestamp fields."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=TIMESTAMP(timezone=True),
        nullable=False,
        sa_column_kwargs=dict(server_default=func.now()),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=TIMESTAMP(timezone=True),
        nullable=False,
        sa_column_kwargs=dict(server_default=func.now(), onupdate=func.now()),
    )


class BaseModel(UUIDMixin, TimeStampedMixin, ABC):
    """
    Abstract base model that standardizes table naming and database structure.

    Table names are derived automatically from class names, following a
    snake_case convention. This class has been designed for extension by
    model classes, not for direct instantiation.
    """

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
