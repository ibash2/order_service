from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.init import init_container
from presentation.api.controllers.main import setup_controllers, setup_middleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
 


def init_api() -> FastAPI:
    app = FastAPI(
        title="User Service",
        docs_url="/api/docs",
        version="1.0.0",
        lifespan=lifespan,
    )
    setup_controllers(app)
    setup_middleware(app)

    return app
