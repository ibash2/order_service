from dataclasses import dataclass

from domain.common.exceptions.base import DomainError


@dataclass(eq=False)
class InfrastructureException(DomainError):
    @property
    def message(self) -> str: # type: ignore
        return "В обработке запроса возникла ошибка."
