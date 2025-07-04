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
from order_service.src.application.order.commands.process_order import (
    ProcessOrderCommand,
    ProcessOrderCommandHandler,
)
from application.order.events.order_created import OrderCreatedEventHandler
from application.order.interfaces.persistence.repo import OrderRepo
from application.order.queries.get_user_orders import (
    GetUserOrdersQuery,
    GetUserOrdersQueryHandler,
)
from application.common.event import MediatorProtocol
from application.order.interfaces.persistence.reader import OrderReader, UserReader
from application.order.commands.create_order import (
    CreateOrderCommand,
    CreateOrderCommandHandler,
)
from order_service.src.domain.order.events.new_order import OrderCreatedEvent
from order_service.src.domain.order.events.order_updated import OrderUpdatedEvent
from order_service.src.infrastructure.persistence.db.repositories.order import (
    SqlAlchemyOrderRepository,
)


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
        return RabbitMessageBroker(
            config=EventBusConfig(host=config.MQ_HOST, port=int(config.MQ_PORT))
        )

    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton,
    )

    # Repositories
    container.register(OrderRepo, SqlAlchemyOrderRepository)

    # Readers
    container.register(OrderReader, SqlAlchemyOrderRepository)

    # Mediator
    mediator = Mediator(container)

    # commands
    mediator.register_command(CreateOrderCommand, CreateOrderCommandHandler)
    mediator.register_command(ProcessOrderCommand, ProcessOrderCommandHandler)

    # queries
    mediator.register_query(GetUserOrdersQuery, GetUserOrdersQueryHandler)

    # event
    mediator.register_event(
        OrderCreatedEvent,
        OrderCreatedEventHandler,
        broker_topic=config.order_created_topic,
    )
    # mediator.register_event(
    #     OrderUpdatedEvent,
    #     OrderUpdatedEventHandler,
    #     broker_topic=config.order_updated_topic,
    # )

    container.register(Mediator, instance=mediator)
    container.register(MediatorProtocol, instance=mediator)
    container.register(EventMediator, instance=mediator)
    container.register(QueryMediator, instance=mediator)
    container.register(CommandMediator, instance=mediator)

    return container
