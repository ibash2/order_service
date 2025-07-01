import asyncio
import sys
import json
import logging

from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.init import init_container
from infrastructure.log.main import configure_logging, LoggingConfig

logger = logging.Logger("socket_manager")
logger.addHandler(logging.StreamHandler(sys.stdout))
configure_logging(LoggingConfig(level="INFO"))

container = init_container()


async def callback(ch, method, properties, data):
    logger.info(f" [x] public {data}")

    try:
        if data["action"] == "run_socket":
            await sokets_manager.run_socket(data["data"]["wallet_id"])

        if data["action"] == "stop_socket":
            await sokets_manager.stop_socket(data["data"]["wallet_id"])

    except Exception as e:
        logger.exception(e)


async def main():
    rmq: BaseMessageBroker = container.resolve(BaseMessageBroker)  # type: ignore
    await rmq.start()

    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    async for message in rmq.start_consuming(topic="user_socket_manager"):  # type: ignore
        await callback(None, None, None, message)  # type: ignore


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)
