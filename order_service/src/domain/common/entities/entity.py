from abc import ABC
from copy import copy
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID, uuid4
from datetime import datetime

from domain.common.events.event import Event


@dataclass
class Entity(ABC):
    id: UUID = field(
        default_factory=uuid4,
        kw_only=True,
    )
    _events: list[Event] = field(
        default_factory=list,
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: "Entity") -> bool:
        return self.id == __value.id

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def pull_events(self) -> list[Event]:
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events
