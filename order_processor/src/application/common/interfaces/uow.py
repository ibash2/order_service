from typing import Protocol


class UnitOfWork(Protocol):
    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
