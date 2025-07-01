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


VT = TypeVar('VT', bound=Any)

@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self):
        self._validate()


    def _validate(self):
        ...


@dataclass(frozen=True)
class ValueObject(ABC, Generic[VT]):
    value: VT

    def as_generic_type(self) -> VT:
        ...
