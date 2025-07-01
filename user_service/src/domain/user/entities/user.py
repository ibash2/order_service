from dataclasses import dataclass

from domain.common.entities import AggregateRoot
from domain.user.events.new_pair import UserCreatedEvent

@dataclass
class User(AggregateRoot):
    login: str 
    password: str

    @classmethod
    def create(cls, login: str, password: str) -> "User":
        user = cls(login=login, password=password)
        user.register_event(
            event=UserCreatedEvent(
                user_id=str(user.id),
                login=user.login,
            )
        )
        return user