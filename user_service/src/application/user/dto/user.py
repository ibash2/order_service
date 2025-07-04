from decimal import Decimal
from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from application.common.dto import DTO


@dataclass
class UserDto(DTO):
    id: UUID
    login: str
