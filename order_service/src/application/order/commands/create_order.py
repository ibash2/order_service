from dataclasses import dataclass
import logging
from uuid import UUID

from application.common.command import Command
from application.common.command import CommandHandler
from application.common.interfaces.uow import UnitOfWork
from domain.order.entities.order import Order
from application.order.interfaces.persistence.repo import OrderRepo

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateOrderCommand(Command):
    user_id: str
    amount: float


@dataclass(frozen=True)
class CreateOrderCommandHandler(CommandHandler[CreateOrderCommand, UUID]):
    uow: UnitOfWork
    order_repo: OrderRepo

    async def handle(self, command: CreateOrderCommand) -> UUID:
        order = Order.create(command.user_id, command.amount)

        async with self.uow:
            await self.order_repo.add_order(order)
            await self._mediator.publish(order.pull_events())
            await self.uow.commit()

            logger.info("Order created", extra={"order": order})

        return order.id
