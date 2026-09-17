from enum import Enum
from typing import Annotated, Literal, TypeVar

from pydantic import BaseModel, Field

_ResponseT = TypeVar('_ResponseT', bound=BaseModel | dict | list)
"""Dynamic response type.

Bəzi API-lər (məs., E-Customs) kök səviyyəsində JSON array qaytarır, ona görə
`list` də bound-a daxildir (`APIResponse[list[SomeSchema]]`).
"""

T = TypeVar('T')


class UnsetType:
    """Sentinel type to indicate an unset field value."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return '<UNSET>'

    def __str__(self):
        return 'UNSET'

    def __bool__(self):
        return False


UNSET = UnsetType()

Unset = T | Literal[UNSET]
""" Optional argument tipi """

UnsetOrNone = T | Literal[UNSET] | None
"""None dəyəri ala bilən optional argument tipi"""

UnsetField = Annotated[Unset[T], Field(default=UNSET, exclude_if=lambda x: x is UNSET)]
"""Pydantic üçün set olunmamış argument dəyəri"""

UnsetOrNoneField = Annotated[UnsetOrNone[T], Field(default=UNSET, exclude_if=lambda x: x is UNSET)]
"""Pydantic üçün set olunmamış və None dəyəri ala bilən argument dəyəri"""


class Environment(str, Enum):
    TEST = 'test'
    PROD = 'prod'
