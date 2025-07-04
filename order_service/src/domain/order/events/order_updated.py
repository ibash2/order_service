from dataclasses import dataclass
from typing import ClassVar

from domain.common.events.event import Event


@dataclass
class OrderUpdatedEvent(Event):
    event_title: ClassVar[str] = "Order Updated Event."
    order_id: str
