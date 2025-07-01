from dataclasses import dataclass
from typing import ClassVar

from domain.common.events.event import Event


@dataclass
class UserCreatedEvent(Event):
    event_title: ClassVar[str] = "User Created Event." 
    
    user_id: str
    login: str