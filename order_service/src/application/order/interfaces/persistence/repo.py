import abc
from typing import Protocol

from domain.order import entities
from domain.order.entities.order import Order


class OrderRepo(Protocol):
    @abc.abstractmethod
    async def get_order(self, order_id: str) -> Order | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_order(self, order: entities.Order) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_order(self, order: entities.Order) -> None:
        raise NotImplementedError
