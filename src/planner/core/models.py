import re
from abc import ABC
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel


def camel_to_snake(camel_str: str) -> str:
    """
    Convert a CamelCase string to snake_case.

    The implementation of this function is taken directly from the accepted answer
    to a StackOverflow question. See the following URL for reference:

    https://shorturl.at/hABI1


    Args:
        camel_str: a string in CamelCase format.

    Returns:
        A string in snake_case format.
    """
    # Add underscore before uppercase followed by lowercase
    temp_str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    # Add underscore before lowercase or digit followed by uppercase
    snake_str = re.sub("([a-z0-9])([A-Z])", r"\1_\2", temp_str)

    return snake_str.lower()


class UUIDMixin(SQLModel):
    """Mixin class that adds a unique UUID field."""

    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs=dict(server_default=text("gen_random_uuid()"), unique=True),
    )


class TimeStampedMixin(SQLModel):
    """Mixin class that adds created and modified timestamp fields."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs=dict(server_default=func.now()),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs=dict(
            server_default=func.now(),
            onupdate=func.now(),
        ),
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
