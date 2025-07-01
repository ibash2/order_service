from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(InfrastructureException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(InfrastructureException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для команды: {self.command_type}"
