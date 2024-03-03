from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseError(ABC, Exception):
    """Abstract base class for custom exceptions."""

    message: str

    def __post_init__(self) -> None:
        super().__init__(self.message)
