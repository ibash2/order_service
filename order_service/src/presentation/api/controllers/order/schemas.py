from dataclasses import asdict, dataclass
from pydantic import BaseModel

from presentation.api.controllers.schemas import BaseQueryResponseSchema


class CreateOrderRequest(BaseModel):
    amount: float
