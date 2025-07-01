from dataclasses import dataclass

import orjson

from application.common.event import EventHandler
from domain.user.events.new_pair import UserCreatedEvent
from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class UserCreatedEventHandler(EventHandler[UserCreatedEvent, None]):
    broker_topic: str
    message_broker: BaseMessageBroker

    async def handle(self, event: UserCreatedEvent) -> None:
        # TODO Нужен конвертер
        message = orjson.dumps(event)

        await self.message_broker.send_message(self.broker_topic, message)
        return None
