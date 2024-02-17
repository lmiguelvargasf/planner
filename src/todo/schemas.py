from datetime import datetime

from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str = "up"


class TodoItem(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
