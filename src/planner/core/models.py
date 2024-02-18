import re
import uuid as _uuid
from datetime import UTC, datetime

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


class BaseModel(SQLModel):
    uuid: _uuid.UUID = Field(
        default_factory=_uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs=dict(server_default=text("gen_random_uuid()"), unique=True),
    )

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

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
