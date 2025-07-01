from dataclasses import dataclass
from infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class RequestException(InfrastructureException):
    @property
    def message(self):
        return "Ошибка запроса"


@dataclass(eq=False)
class ChartDataNotAvailableException(InfrastructureException):
    @property
    def message(self):
        return "Данные графика не доступны"
