from enum import Enum
from dataclasses import dataclass, field

from domain.common.entities import AggregateRoot
from order_processor.src.domain.order.events.new_order import OrderCreatedEvent
from order_processor.src.domain.order.events.order_updated import OrderUpdatedEvent


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Order(AggregateRoot):
    user_id: str
    amount: float
    status: OrderStatus = field(default=OrderStatus.PENDING, kw_only=True)

    @classmethod
    def create(cls, user_id: str, amount: float) -> "Order":
        order = cls(user_id=user_id, amount=amount)
        order.register_event(
            event=OrderCreatedEvent(
                order_id=str(order.id),
            )
        )
        return order

    def update_status(self, status: OrderStatus):
        self.status = status
        self.register_event(
            event=OrderUpdatedEvent(
                order_id=str(self.id),
            )
        )
