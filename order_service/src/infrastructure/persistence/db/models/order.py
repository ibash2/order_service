from typing import Any, ClassVar
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class Order(TimedBaseModel):
    __tablename__ = "order"
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
