from dataclasses import dataclass

from application.order import dto
from application.common.interfaces.uow import UnitOfWork
from application.common.query import Query, QueryHandler
from application.order.interfaces.persistence.reader import OrderReader


@dataclass(frozen=True)
class GetUserOrdersQuery(Query):
    user_id: str


@dataclass(frozen=True)
class GetUserOrdersQueryHandler(QueryHandler[GetUserOrdersQuery, dto.Orders]):
    uow: UnitOfWork
    order_reader: OrderReader

    async def handle(self, query: GetUserOrdersQuery) -> dto.Orders:
        orders = await self.order_reader.get_orders(query.user_id)
        return orders
