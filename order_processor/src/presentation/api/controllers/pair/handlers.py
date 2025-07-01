import time
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from application.user import dto
from user_service.src.application.user.queries.get_user import GetUserQuery
from infrastructure.init import resolve_mediator
from infrastructure.mediator.base import Mediator
from presentation.api.controllers.schemas import ErrorSchema
from presentation.api.controllers.auth.jwt import parse_jwt_user_data, JWTData

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/user",
    description="Эндпоинт отдает пользователя.",
    responses={
        status.HTTP_200_OK: {"model": },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def trending(
    token: JWTData = Depends(parse_jwt_user_data),
    mediator: Mediator = Depends(resolve_mediator),
):
    # Handle query
    user = await mediator.handle_query(
    )
    return user

