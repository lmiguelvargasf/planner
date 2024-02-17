from datetime import datetime

import pytest

from src.todo.models import TodoItem


def test_todo_item_creation_with_valid_data():
    todo_item = TodoItem(title="Test Task")
    todo_item_db = TodoItem.model_validate(todo_item)
    assert todo_item_db.title == "Test Task"
    assert todo_item_db.completed is False
    assert isinstance(todo_item_db.created_at, datetime)


def test_todo_item_creation_with_invalid_data():
    with pytest.raises(ValueError):
        TodoItem.model_validate(TodoItem(title=123))
