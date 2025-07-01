from pydantic import BaseModel

from presentation.api.controllers.auth import jwt


class AuthResponseSchema(BaseModel):
    status: str
    token: str

    @classmethod
    def from_user_entity(cls, user: User) -> "AuthResponseSchema":
        return cls(status="success", token=jwt.create_access_token(user_id=user.id))

    @classmethod
    def from_data(cls, data: str) -> "AuthResponseSchema":
        return cls(status="success", token=data)
