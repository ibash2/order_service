from functools import lru_cache
from urllib.parse import urlparse

from punq import (
    Container,
    Scope,
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from application.user.queries.get_user import (
    GetUserQuery,
    GetPairTransactionsQueryHandler,
    GetTransactionsStatsQuery,
    GetTransactionsStatsQueryHandler,
)
from application.common.event import MediatorProtocol
from application.user.interfaces.persistence.reader import UserReader
from application.user.commands.create_user import CreateUserCommand, CreateUserCommandHandler
from user_service.src.infrastructure.persistence.db.repositories.user import BasePairRepository, SqlAlchemyPairRepository


from infrastructure.mediator.base import Mediator
from infrastructure.mediator.command import CommandMediator
from infrastructure.mediator.event import EventMediator
from infrastructure.mediator.query import QueryMediator
from infrastructure.message_brokers.config import EventBusConfig
from infrastructure.uow import UnitOfWork
from infrastructure.persistence.db.repositories.base import (
    build_sa_engine,
    build_sa_session_factory,
)
from infrastructure.persistence.db.uow import SQLAlchemyUoW
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.rmq import RabbitMessageBroker

from settings.config import Config
from user_service.src.application.user.events.user_created import UserCreatedEventHandler
from user_service.src.domain.user.events.new_pair import UserCreatedEvent


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def resolve_mediator() -> Mediator:
    container = init_container()
    return container.resolve(Mediator)  # type: ignore


def _init_container() -> Container:
    container = Container()

    # Configs
    container.register(Config, instance=Config())  # type: ignore
    config: Config = container.resolve(Config)  # type: ignore

  
    # Database
    container.register(
        AsyncEngine,
        instance=build_sa_engine(config),
        scope=Scope.singleton,
    )
    container.register(
        async_sessionmaker[AsyncSession],
        instance=build_sa_session_factory(container.resolve(AsyncEngine)),  # type: ignore
    )
    container.register(SQLAlchemyUoW, SQLAlchemyUoW)
    container.register(UnitOfWork, SQLAlchemyUoW)

    # Message Broker
    def create_message_broker() -> BaseMessageBroker:
        return RabbitMessageBroker(config=EventBusConfig(host=config.MQ_HOST, port=int(config.MQ_PORT)))

    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton,
    )
  
    # Repositories
    container.register(BasePairRepository, SqlAlchemyPairRepository)

    # Readers
    container.register(UserReader, PASS)


    # Mediator
    mediator = Mediator(container)

    # commands
    mediator.register_command(CreateUserCommand, CreateUserCommandHandler)
    
    # queries
    mediator.register_query(GetUserQuery, GetPairTransactionsQueryHandler)
    mediator.register_query(GetTransactionsStatsQuery, GetTransactionsStatsQueryHandler)

    # event
    mediator.register_event(UserCreatedEvent, UserCreatedEventHandler, broker_topic=config.user_created_topic)

    container.register(Mediator, instance=mediator)
    container.register(MediatorProtocol, instance=mediator)
    container.register(EventMediator, instance=mediator)
    container.register(QueryMediator, instance=mediator)
    container.register(CommandMediator, instance=mediator)

    return container
