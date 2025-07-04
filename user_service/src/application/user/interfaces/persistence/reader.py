from typing import Protocol

import abc

from application.user import dto


class UserReader(Protocol):
    @abc.abstractmethod
    async def get_user(self, user_id: str) -> dto.UserDto: ...
