from typing import Protocol

import abc

from application.order import dto


class OrderReader(Protocol):
    @abc.abstractmethod
    async def get_orders(self, user_id: str) -> dto.Orders: ...
