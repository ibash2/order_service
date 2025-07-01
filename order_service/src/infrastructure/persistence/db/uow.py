import logging
from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)

from infrastructure.persistence.db.repositories.base import db_session_context_var



logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyUoW:
    _session_factory: async_sessionmaker[AsyncSession]

    async def __aenter__(self) -> "SQLAlchemyUoW":
        self._session = self._session_factory()
        self._token = db_session_context_var.set(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self._session.rollback()
            # else:
            #     await self._session.commit()
        except SQLAlchemyError:
            await self._session.rollback()
            raise
        finally:
            await self._session.close()
            db_session_context_var.reset(self._token)

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError:
            await self._session.rollback()
            raise

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError:
            raise

    @property
    def session(self) -> AsyncSession:
        return self._session
