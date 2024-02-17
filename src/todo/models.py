from sqlmodel import Field

from ..core.models import BaseModel


class TodoItem(BaseModel, table=True):
    title: str
    description: str | None
    completed: bool = Field(
        default=False, sa_column_kwargs=dict(server_default="FALSE")
    )
