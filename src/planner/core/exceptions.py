from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseError(ABC, Exception):
    """Abstract base class for custom exceptions."""

    message: str
