from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)
from typing import Any, Protocol, Type, runtime_checkable

from domain.common.events.event import Event




@runtime_checkable
class EventHandlerProtocol(Protocol):
    async def handle(self, event: Event) -> Any: ...


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[Type[Event], list[Type[EventHandlerProtocol]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(
        self, event: Type[Event], event_handler: Type[EventHandlerProtocol], **kwargs
    ): ...

    @abstractmethod
    async def publish(self, events: Iterable[Event]) -> Iterable[Any]: ...
