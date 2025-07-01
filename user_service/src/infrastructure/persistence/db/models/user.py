from typing import Any, ClassVar
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "user"
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)