import pytest
from planner.users.models import Sex, User


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


def test_user_sex_validation():
    male_user = User(email="male@example.com", sex=Sex.MALE)
    female_user = User(email="female@example.com", sex=Sex.FEMALE)
    user_with_invalid_sex = User(email="invalid@example.com", sex="invalid")

    male_user_db = User.model_validate(male_user)
    female_user_db = User.model_validate(female_user)

    assert male_user_db.sex == Sex.MALE
    assert female_user_db.sex == Sex.FEMALE

    with pytest.raises(ValueError, match="sex"):
        User.model_validate(user_with_invalid_sex)
