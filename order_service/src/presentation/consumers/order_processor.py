import asyncio
import random
import sys
import json
import logging

from application.order.commands.process_order import ProcessOrderCommand
from settings.config import Config
from infrastructure.init import init_container
from infrastructure.mediator.base import Mediator
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.log.main import configure_logging, LoggingConfig

logger = logging.Logger("order-processor")
configure_logging(LoggingConfig(level="INFO"))

container = init_container()


async def main():
    container = init_container()
    config: Config = container.resolve(Config)  # type: ignore
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)  # type: ignore

    mediator: Mediator = container.resolve(Mediator)  # type: ignore
    await message_broker.start()

    async def process(order_id: str):
        await asyncio.sleep(random.randint(2, 5))
        await mediator.publish(
            [
                ProcessOrderCommand(
                    order_id=order_id,
                ),
            ]
        )

    async for msg in message_broker.start_consuming(config.order_created_topic):  # type: ignore
        asyncio.create_task(process(msg["order_id"]))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)
