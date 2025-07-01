from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings.config import Config

from .default import default_router
from .exceptions import setup_exception_handlers
from .healthcheck import healthcheck_router
from .auth.handlers import router as auth_router
from .pair.handlers import router as pair_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(healthcheck_router)
    app.include_router(auth_router)
    app.include_router(pair_router)
    setup_exception_handlers(app)


def setup_middleware(app: FastAPI) -> None:
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.ALLOW_ORIGINS,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=["*"],  # Expose all headers
        max_age=86400,  # Cache preflight requests for 24 hours
    )