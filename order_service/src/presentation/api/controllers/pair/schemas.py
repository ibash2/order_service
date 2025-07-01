
from dataclasses import asdict, dataclass
from pydantic import BaseModel

from presentation.api.controllers.schemas import BaseQueryResponseSchema

from application.user.dto.pair import PairDto


@dataclass
class PairDetailSchema(PairDto):
    baseimg: str = "/pair/{}.svg".format(str("btc").lower())
    quoteimg: str = "/pair/{}.svg".format(str("usdt").lower())

    @classmethod
    def from_dto(cls, dto: PairDto):
        return cls(
            id=dto.id,
            symbol=dto.symbol,
            base=dto.base,
            quote=dto.quote,
            precision=dto.precision,
            limits=dto.limits,
            # baseimg="/pair/{}.svg".format(str(dto.base).lower()),
            # quoteimg="/pair/{}.svg".format(str(dto.quote).lower()),
        )


class GetPairInfoResponseSchema(BaseQueryResponseSchema[list[PairDetailSchema]]): ...


class GetPriceResponseSchema(BaseModel):
    status: str = "success"
    price: float | None
