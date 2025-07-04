from dataclasses import dataclass

from sqlalchemy import select

from application.order import dto

from infrastructure.persistence.db.repositories.base import SQLAlchemyRepo
from infrastructure.persistence.db.converters import (
    convert_db_model_to_order_dto,
    convert_order_entity_to_db_model,
    convert_db_model_to_order_entity,
)
from order_service.src.domain.order import entities
from order_service.src.infrastructure.persistence.db import models


@dataclass
class SqlAlchemyOrderRepository(SQLAlchemyRepo):
    async def add_order(self, order: entities.Order) -> None:
        self.session.add(convert_order_entity_to_db_model(order))
        await self.session.flush()

    async def update_order(self, order: entities.Order) -> None:
        self.session.merge(convert_order_entity_to_db_model(order))
        await self.session.flush()

    async def get_orders(self, user_id: str) -> dto.Orders:
        query = select(models.Order).where(models.Order.user_id == user_id)
        result = await self.session.scalars(query)
        return [convert_db_model_to_order_dto(order) for order in result]

    async def get_order(self, order_id: str) -> entities.Order | None:
        query = select(models.Order).where(models.Order.order_id == order_id)
        result = await self.session.scalar(query)
        if not result:
            result
        return convert_db_model_to_order_entity(result)
