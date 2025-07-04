from dataclasses import dataclass
from typing import ClassVar

from domain.common.events.event import Event


@dataclass
class OrderCreatedEvent(Event):
    event_title: ClassVar[str] = "Order Created Event."
    order_id: str
