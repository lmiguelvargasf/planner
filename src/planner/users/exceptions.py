from dataclasses import dataclass
from enum import Enum

from ..core.exceptions import BaseError


class UserErrorMessage(Enum):
    DUPLICATE_EMAIL = "A user with this email already exists."
    NOT_FOUND_BY_UUID = "The user for the provided UUID does not exist."
    NOT_FOUND_BY_EMAIL = "The user for the provided email does not exist."


@dataclass
class UserError(BaseError):
    ...
