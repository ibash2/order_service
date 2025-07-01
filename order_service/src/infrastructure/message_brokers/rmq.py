import json
from typing import Iterator
from dataclasses import dataclass, field

import orjson
import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue


from infrastructure.message_brokers.config import EventBusConfig
from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class RabbitMessageBroker(BaseMessageBroker):
    config: EventBusConfig

    _channel: AbstractChannel | None = field(init=False, default=None)
    _connection: AbstractRobustConnection | None = field(init=False, default=None)

    async def start(self):
        if self._connection or self._channel:
            return 
        self._connection = await aio_pika.connect_robust(
            host=self.config.host,
            port=self.config.port,
            login=self.config.login,
            password=self.config.password,
        )
        self._channel = await self._connection.channel()

    async def close(self):
        if self._connection is None or self._channel is None:
            raise ValueError("RMQ is not started")

        await self._connection.close()
        await self._channel.close()

    async def send_message(self, queue: str, value: bytes):
        if self._channel is None:
            raise ValueError("RMQ channel is not stated")

        await self._declare_queue(queue)
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=value), routing_key=queue
        )

    async def start_consuming(self, topic: str):
        async with self._connection:
            queue = await self._declare_queue(topic)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    yield orjson.loads(message.body)

    async def stop_consuming(self, topic: str):
        if self._connection is None or self._channel is None:
            raise ValueError("RMQ is not started")

        await self._connection.close()
        await self._channel.close()

    async def _declare_queue(self, queue_name: str) -> AbstractQueue:
        if self._channel is None:
            raise ValueError("RMQ channel is not stated")
        return await self._channel.declare_queue(queue_name, auto_delete=True)
