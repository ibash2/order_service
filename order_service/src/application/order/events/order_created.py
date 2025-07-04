from dataclasses import dataclass

import orjson

from application.common.event import EventHandler
from domain.order.events.new_order import OrderCreatedEvent
from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class OrderCreatedEventHandler(EventHandler[OrderCreatedEvent, None]):
    broker_topic: str
    message_broker: BaseMessageBroker

    async def handle(self, event: OrderCreatedEvent) -> None:
        # TODO Нужен конвертер
        message = orjson.dumps(event)

        await self.message_broker.send_message(self.broker_topic, message)
        return None
