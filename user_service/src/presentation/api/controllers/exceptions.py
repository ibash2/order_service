from functools import partial
import logging
from collections.abc import (
    Awaitable,
    Callable,
)

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from presentation.api.controllers.auth.exceptions import AuthException
from presentation.api.controllers.responses.orjson import ORJSONResponse
from presentation.api.controllers.schemas import ErrorSchema

from domain.common.exceptions.base import  AppError


logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        AppError, error_handler(status_code=status.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        AuthException, error_handler(status_code=status.HTTP_401_UNAUTHORIZED)
    )
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: AppError, status_code: int
) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        message=err.message,
        status_code=status_code,
    )


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorSchema(error=err.__class__.__name__).model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    message: str,
    status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", extra={"error": err})
    return ORJSONResponse(
        content=ErrorSchema(error=message).model_dump(),
        status_code=status_code,
    )
