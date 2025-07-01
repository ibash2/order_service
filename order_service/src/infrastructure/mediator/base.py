import logging
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    asdict,
    dataclass,
    field,
    is_dataclass,
)
from typing import Any, Type

from punq import Container

from application.common.command import Command, CommandHandler
from application.common.event import Event, EventHandler
from application.common.query import Query, QueryHandler
from infrastructure.exceptions.mediator import CommandHandlersNotRegisteredException
from infrastructure.mediator.command import CommandMediator
from infrastructure.mediator.event import EventMediator
from infrastructure.mediator.query import QueryMediator


logger = logging.getLogger("mediator")


def safe_asdict(obj):
    if not is_dataclass(obj):
        return str(obj)

    result = {}
    for field in obj.__dataclass_fields__:
        val = getattr(obj, field)
        try:
            result[field] = asdict(val) if is_dataclass(val) else str(val)
        except Exception:
            result[field] = "<unserializable>"
    return result


@dataclass(eq=False)
class Mediator(EventMediator, QueryMediator, CommandMediator):
    container: Container
    events_map: dict[Type[Event], list[Type[EventHandler]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[Type[Command], list[Type[CommandHandler]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[Type[Query], Type[QueryHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(
        self,
        event: Type[Event],
        event_handler: Type[EventHandler],
        **kwargs,
    ):
        self.container.register(event_handler, event_handler, **kwargs)
        self.events_map[event].append(event_handler)

    def register_command(
        self,
        command: Type[Command],
        command_handler: Type[CommandHandler],
    ):
        self.container.register(command_handler)
        self.commands_map[command].append(command_handler)

    def register_query(
        self,
        query: Type[Query],
        query_handler: Type[QueryHandler],
    ) -> Any:
        self.container.register(query_handler)
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[Event]) -> Iterable[Any]:
        result = []

        for event in events:
            logger.debug(f"{event} occurred", extra={"event_data": asdict(event)})
            handlers: Iterable[Type[EventHandler]] = self.events_map[event.__class__]
            for handler in handlers:
                handler_instance = self.container.resolve(handler)
                if hasattr(handler_instance, "handle"):
                    result.append(await handler_instance.handle(event))

        return result

    async def handle_command(self, command: Command) -> Iterable[Any]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)
        logger.debug(f"{command} occurred", extra={"event_data": safe_asdict(command)})

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        result = []
        for handler in handlers:
            handler_instance = self.container.resolve(handler)
            if hasattr(handler_instance, "handle"):
                result.append(await handler_instance.handle(command))

        return result

    async def handle_query(self, query: Query) -> Any:
        logger.debug(f"{query} occurred", extra={"event_data": asdict(query)})
        handler_class = self.queries_map.get(query.__class__)
        if handler_class:
            handler = self.container.resolve(handler_class)
            if hasattr(handler, "handle"):
                return await handler.handle(query=query)
        return None
