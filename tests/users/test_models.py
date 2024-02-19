from datetime import date

import pytest
from planner.users.models import Sex, User


def test_user_creation_minimum_data():
    user = User(email="user@example.com")
    db_user = User.model_validate(user)

    assert db_user.first_name is None
    assert db_user.middle_name is None
    assert db_user.last_name is None
    assert db_user.second_last_name is None
    assert db_user.date_of_birth is None
    assert db_user.sex is None
    assert db_user.email == "user@example.com"
    assert db_user.hashed_password is None
    assert db_user.is_active is True
    assert db_user.is_superuser is False


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

    db_male_user = User.model_validate(male_user)
    db_female_user = User.model_validate(female_user)

    assert db_male_user.sex == Sex.MALE
    assert db_female_user.sex == Sex.FEMALE

    with pytest.raises(ValueError, match="sex"):
        User.model_validate(user_with_invalid_sex)


def test_user_date_of_birth_validation():
    user = User(email="user@example.com", date_of_birth=date(1990, 1, 1))
    user_with_invalid_date_of_birth = User(
        email="invalid@example.com", date_of_birth="not a date"
    )

    db_user = User.model_validate(user)

    assert db_user.date_of_birth == date(1990, 1, 1)

    with pytest.raises(ValueError, match="date_of_birth"):
        User.model_validate(user_with_invalid_date_of_birth)


def test_user_creation_full_data():
    user = User(
        first_name="John",
        middle_name="James",
        last_name="Smith",
        second_last_name="Wilson",
        date_of_birth=date(1980, 5, 20),
        sex=Sex.MALE,
        email="john.smith@example.com",
        hashed_password="password",
        is_active=False,
        is_superuser=True,
    )
    db_user = User.model_validate(user)

    assert db_user.first_name == "John"
    assert db_user.middle_name == "James"
    assert db_user.last_name == "Smith"
    assert db_user.second_last_name == "Wilson"
    assert db_user.date_of_birth == date(1980, 5, 20)
    assert db_user.sex == Sex.MALE
    assert db_user.email == "john.smith@example.com"
    assert db_user.hashed_password.get_secret_value() == "password"
    assert db_user.is_active is False
    assert db_user.is_superuser is True
