from dataclasses import dataclass

from domain.common.exceptions import AppError


class ApplicationError(AppError):
    """Base Application Exception."""

    @property
    def message(self) -> str:
        return "An application error occurred"


class UnexpectedError(ApplicationError):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass


@dataclass(eq=False)
class MappingError(ApplicationError):
    _text: str

    @property
    def message(self) -> str:
        return self._text


@dataclass(eq=False)
class EventHandlersNotRegisteredException(ApplicationError):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(ApplicationError):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для команды: {self.command_type}"
