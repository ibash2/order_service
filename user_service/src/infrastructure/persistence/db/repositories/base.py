from contextvars import ContextVar
from dataclasses import dataclass, field
from collections.abc import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings.config import Config

db_session_context_var = ContextVar("db_session")


@dataclass
class SQLAlchemyRepo:
    __session: AsyncSession | None = field(
        default=None,
        init=False,
    )

    @property
    def session(self) -> AsyncSession:
        if self.__session is not None:
            if not self.__session.in_transaction():
                self.__session = None
            else:
                return self.__session

        self.__session = db_session_context_var.get()
        return self.__session    # type: ignore


def build_sa_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        str(config.DATABASE_URL),
        # echo=True,
        # echo_pool=config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=100,
    )
    return engine


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
