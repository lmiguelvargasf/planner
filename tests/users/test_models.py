from datetime import date

import pytest
from planner.users.models import Sex, User


def test_user_creation_minimum_data():
    user = User(email="user@example.com")
    user_db = User.model_validate(user)

    assert user_db.first_name is None
    assert user_db.middle_name is None
    assert user_db.last_name is None
    assert user_db.second_last_name is None
    assert user_db.date_of_birth is None
    assert user_db.sex is None
    assert user_db.email == "user@example.com"
    assert user_db.hashed_password is None
    assert user_db.is_active is True
    assert user_db.is_superuser is False


def test_user_email_validation():
    user_with_no_email = User()
    user_with_invalid_email = User(email="hi")

    with pytest.raises(ValueError, match="email"):
        User.model_validate(user_with_no_email)

    with pytest.raises(ValueError, match="email address is not valid"):
        User.model_validate(user_with_invalid_email)


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


def test_user_date_of_birth_validation():
    user = User(email="user@example.com", date_of_birth=date(1990, 1, 1))
    user_with_invalid_date_of_birth = User(
        email="invalid@example.com", date_of_birth="not a date"
    )

    user_db = User.model_validate(user)

    assert user_db.date_of_birth == date(1990, 1, 1)

    with pytest.raises(ValueError, match="date_of_birth"):
        User.model_validate(user_with_invalid_date_of_birth)
