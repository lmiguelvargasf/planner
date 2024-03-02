from dataclasses import dataclass
from enum import Enum

from ..core.exceptions import BaseError


class UserErrorMessage(Enum):
    DUPLICATE_EMAIL = "A user with this email already exists."


@dataclass
class UserError(BaseError):
    ...
