from ..core.models import BaseModel


class TodoItem(BaseModel, table=True):
    title: str
    description: str | None
    completed: bool = False
