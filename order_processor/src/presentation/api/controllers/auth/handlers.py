from uuid import uuid4
from fastapi import APIRouter, Depends, status

from punq import Container

from application.user.commands.user import AuthCommand, CreateNonceCommand, CreateSessionCommand, WalletAuthCommand
from infrastructure.mediator.base import Mediator
from infrastructure.init import init_container, resolve_mediator
from presentation.api.controllers.schemas import ErrorSchema
from presentation.api.controllers.auth.schemas import (
    AuthResponseSchema,
    CreateNonceResponse,
    InitDataModel,
    WalletAuthRequest,
)
from presentation.api.controllers.auth.dependencies import valid_init_data

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/auth",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт авторизации пользователя",
    responses={
        status.HTTP_201_CREATED: {"model": AuthResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_session(
    container: Container = Depends(init_container),
) -> AuthResponseSchema:
    """Создает временную сессию для пользователя."""
    mediator: Mediator = container.resolve(Mediator)  # type: ignore

    session_id, *_ = await mediator.handle_command(CreateSessionCommand())

    return AuthResponseSchema.from_data(session_id)

