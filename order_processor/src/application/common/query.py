from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)


@dataclass(frozen=True)
class Query(ABC):
    ...


QT = TypeVar('QT', bound=Query)
QR = TypeVar('QR', bound=Any)


@dataclass(frozen=True)
class QueryHandler(ABC, Generic[QT, QR]):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        ...
