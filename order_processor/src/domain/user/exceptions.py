from dataclasses import dataclass

from domain.common.exceptions.base import DomainError


@dataclass(eq=False)
class EmptyTextException(DomainError):

    @property
    def message(self): # type: ignore
        return 'Text has not ben empty'
