import uuid as _uuid
from datetime import UTC, datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel


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
        sa_column_kwargs=dict(server_default=text("current_timestamp(0)")),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs=dict(
            server_default=text("current_timestamp(0)"),
            onupdate=text("current_timestamp(0)"),
        ),
    )
