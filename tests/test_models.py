from datetime import datetime

import pytest
from todo.schemas import TodoItem


def test_todo_item_creation_with_valid_data():
    todo_item = TodoItem(title="Test Task")
    assert todo_item.title == "Test Task"
    assert todo_item.completed is False
    assert isinstance(todo_item.created_at, datetime)


def test_todo_item_creation_with_invalid_data():
    with pytest.raises(ValueError):
        TodoItem(title=123)
