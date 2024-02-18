import pytest
from planner.users.models import User


def test_user_creation_minimum_data():
    user = User(email="user@example.com")
    user_db = User.model_validate(user)

    assert user_db.email == "user@example.com"
    assert user_db.hashed_password is None
    assert user_db.first_name is None
    assert user_db.last_name is None
    assert user_db.is_active is True
    assert user_db.is_superuser is False


def test_user_creation_fails_no_email():
    user = User()

    with pytest.raises(ValueError, match="email"):
        User.model_validate(user)


def test_user_creation_fails_with_invalid_email():
    user = User(email="hi")

    with pytest.raises(ValueError, match="email address is not valid"):
        User.model_validate(user)
