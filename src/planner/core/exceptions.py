from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseError(ABC, Exception):
    """Abstract base class for custom exceptions."""

    message: str

    def __post_init__(self) -> None:
        """Initializes the base Exception with the provided message.

        Since dataclasses automatically generate an `__init__` method that only
        assigns attributes, this method is necessary to ensure the base Exception
        class is properly initialized with the custom message attribute. This
        allows the custom exception to fully integrate with Python's exception
        handling system.
        """
        super().__init__(self.message)
