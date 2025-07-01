import abc
from typing import Protocol

from domain.user import entities

class UserRepo(Protocol):
    @abc.abstractmethod
    async def acquire_user_by_id(self, user_id: str) -> entities.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_user(self, user: entities.User) -> None:
        raise NotImplementedError