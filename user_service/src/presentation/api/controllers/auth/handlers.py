from uuid import uuid4
from fastapi import APIRouter, Depends, status

from punq import Container

from infrastructure.mediator.base import Mediator
from infrastructure.init import resolve_mediator
from application.user.commands.create_user import CreateUserCommand
from presentation.api.controllers.schemas import ErrorSchema
from presentation.api.controllers.auth.schemas import (
    AuthRequestSchema,
    AuthResponseSchema,
)

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
    body: AuthRequestSchema,
    mediator: Mediator = Depends(resolve_mediator),
) -> AuthResponseSchema:
    """Создает временную сессию для пользователя."""
    session_id, *_ = await mediator.handle_command(
        CreateUserCommand(
            login=body.login,
            password=body.password,
        )
    )

    return AuthResponseSchema.from_data(session_id)
