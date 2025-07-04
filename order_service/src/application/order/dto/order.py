from decimal import Decimal
from dataclasses import dataclass
from typing import TypeAlias

from application.common.dto import DTO


@dataclass
class OrderDto(DTO):
    id: str
    user_id: str
    amount: float
    status: str


Orders: TypeAlias = list[OrderDto]
