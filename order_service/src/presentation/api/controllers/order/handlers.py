import time
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from application.order import dto
from application.order.queries.get_user_orders import (
    GetUserOrdersQuery,
)
from infrastructure.init import resolve_mediator
from infrastructure.mediator.base import Mediator
from application.order.commands.create_order import CreateOrderCommand
from presentation.api.controllers.schemas import ErrorSchema
from presentation.api.controllers.order.schemas import CreateOrderRequest
from presentation.api.controllers.auth.jwt import parse_jwt_user_data, JWTData

router = APIRouter(prefix="/user", tags=["Order"])


@router.post(
    "/order",
    description="Эндпоинт создает ордер.",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_order(
    body: CreateOrderRequest,
    token: JWTData = Depends(parse_jwt_user_data),
    mediator: Mediator = Depends(resolve_mediator),
):
    # Handle command
    await mediator.handle_command(
        CreateOrderCommand(
            user_id=token.user_id,
            amount=body.amount,
        )
    )


@router.get(
    "/orders",
    description="Эндпоинт отдает ордера пользователя.",
    responses={
        status.HTTP_200_OK: {"model": dto.Orders},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_orders(
    token: JWTData = Depends(parse_jwt_user_data),
    mediator: Mediator = Depends(resolve_mediator),
):
    # Handle query
    user = await mediator.handle_query(
        GetUserOrdersQuery(
            user_id=token.user_id,
        )
    )
    return user
