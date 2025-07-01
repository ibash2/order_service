from collections.abc import Sequence
from typing import Protocol

from infrastructure.persistence.db.uow import SQLAlchemyUoW


class UnitOfWork(Protocol):
    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError



class UnitOfWorkImpl:
    def __init__(self, uows: Sequence[UnitOfWork]) -> None:
        self._uows = uows

    async def __aenter__(self):
        for uow in self._uows:
            await uow.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for uow in self._uows:
            await uow.__aexit__(exc_type, exc_value, traceback)

    async def commit(self) -> None:
        for uow in self._uows:
            await uow.commit()

    async def rollback(self) -> None:
        for uow in self._uows:
            await uow.rollback()
            

def build_uow(db_uow: SQLAlchemyUoW) -> UnitOfWork:
    uow = UnitOfWorkImpl((db_uow,))
    return uow