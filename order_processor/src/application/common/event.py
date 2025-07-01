from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    Protocol,
    TypeVar,
)

from domain.common.events.event import Event
from infrastructure.message_brokers.base import BaseMessageBroker

ET = TypeVar("ET", bound=Event)
ER = TypeVar("ER", bound=Any)


@dataclass
class IntegrationEvent(Event, ABC): ...


class MediatorProtocol(Protocol):
    async def publish(self, events: list[Event]) -> list[Any]: ...


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    _mediator: MediatorProtocol
    message_broker: BaseMessageBroker

    @abstractmethod
    async def handle(self, event: ET) -> ER: ...
