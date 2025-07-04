from domain.order import entities
from infrastructure.persistence.db import models
from application.order import dto


def convert_order_entity_to_db_model(order: entities.Order) -> models.Order:
    return models.Order(
        id=order.id,
        user_id=order.user_id,
        amount=order.amount,
        status=order.status,
    )


def convert_db_model_to_order_dto(order: models.Order) -> dto.OrderDto:
    return dto.OrderDto(
        id=order.id,
        user_id=order.user_id,
        amount=order.amount,
        status=order.status,
    )


def convert_db_model_to_order_entity(order: models.Order) -> entities.Order:
    return entities.Order(
        id=order.id,
        user_id=order.user_id,
        amount=order.amount,
        status=order.status,
    )
