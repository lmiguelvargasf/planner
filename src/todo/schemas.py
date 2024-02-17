import uuid as _uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    uuid: _uuid.UUID | None = None
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
