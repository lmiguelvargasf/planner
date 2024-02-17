import uuid as _uuid
from datetime import UTC, datetime

from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    uuid: _uuid.UUID = Field(default_factory=lambda: _uuid.uuid4())
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
