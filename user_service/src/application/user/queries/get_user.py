from dataclasses import dataclass

from application.user import dto
from application.common.interfaces.uow import UnitOfWork
from application.common.query import Query, QueryHandler
from application.user.interfaces.persistence.reader import UserReader


@dataclass(frozen=True)
class GetUserQuery(Query):
    user_id: str


@dataclass(frozen=True)
class GetUserQueryHandler(QueryHandler[GetUserQuery, dto.UserDto]):
    uow: UnitOfWork
    user_reader: UserReader

    async def handle(self, query: GetUserQuery) -> dto.UserDto:
        async with self.uow:
            user = await self.user_reader.get_user(query.user_id)

        return user
