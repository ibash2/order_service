from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from application.common.query import (
    Query,
    QueryHandler,
    QR,
    QT,
)


@dataclass(eq=False)
class QueryMediator(ABC):
    queries_map: dict[QT, type[QueryHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: type[QueryHandler[QT, QR]]) -> QR:
        ...

    @abstractmethod
    async def handle_query(self, query: Query) -> QR:
        ...
