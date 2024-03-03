from dataclasses import dataclass
from enum import StrEnum

from ..core.exceptions import BaseError


class UserErrorMessage(StrEnum):
    DUPLICATE_EMAIL = "A user with this email already exists."
    NOT_FOUND_BY_UUID = "The user for the provided UUID does not exist."
    NOT_FOUND_BY_EMAIL = "The user for the provided email does not exist."
    EMAIL_REQUIRED = "The user's email is required."


@dataclass
class UserError(BaseError):
    ...
