from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from presentation.api.controllers.auth.exceptions import AuthRequired, InvalidToken


oauth2_scheme = HTTPBearer(scheme_name="JWTBearer", bearerFormat="jwt")


# @dataclass
class JWTConfig(BaseSettings):
    exp: int = Field(alias="JWT_EXPIRE_TIME")
    secret: str = Field(alias="JWT_SECRET")
    alg: str = Field(alias="JWT_ALG")


settings = JWTConfig()  # type: ignore


class JWTData(BaseModel):
    id: str


@dataclass
class JWTValidator:
    config: JWTConfig

    def create_access(self, user_id: int) -> str:
        jwt_data = {
            "id": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.config.exp),
        }
        return jwt.encode(jwt_data, self.config.secret, algorithm=self.config.alg)

    # def decode_token(self, token: str) -> JWTData:
    #     return


def create_access_token(
    *,
    user_id: str,
    expires_delta: timedelta = timedelta(minutes=settings.exp),
) -> str:
    jwt_data = {
        "id": str(user_id),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(jwt_data, settings.secret, algorithm=settings.alg)


async def parse_jwt_user_data_optional(
    token: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme),
) -> JWTData | None:

    if not token:
        return None

    try:
        payload = jwt.decode(
            token.credentials,
            settings.secret,
            algorithms=[settings.alg],
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token
