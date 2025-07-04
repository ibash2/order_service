from dataclasses import dataclass

from sqlalchemy import select

from domain.user import entities
from infrastructure.persistence.db.repositories.base import SQLAlchemyRepo
from infrastructure.persistence.db.converters import convert_user_entity_to_db_model
from infrastructure.persistence.db import models


@dataclass
class SqlAlchemyUserRepository(SQLAlchemyRepo):
    async def add_user(self, user: entities.User) -> None:
        user_db_model = convert_user_entity_to_db_model(user)
        self.session.add(user_db_model)
        await self.session.flush()

    async def get_user(self, user_id: str) -> entities.User:
        stmt = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def acquire_user_by_id(self, user_id: str) -> entities.User:
        stmt = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
