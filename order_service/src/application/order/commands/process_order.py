from dataclasses import dataclass
import logging
import random
from uuid import UUID

from application.common.command import Command
from application.common.command import CommandHandler
from application.common.interfaces.uow import UnitOfWork
from domain.order.entities.order import Order, OrderStatus
from application.order.interfaces.persistence.repo import OrderRepo

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessOrderCommand(Command):
    order_id: str


@dataclass(frozen=True)
class ProcessOrderCommandHandler(CommandHandler[ProcessOrderCommand, None]):
    uow: UnitOfWork
    order_repo: OrderRepo

    async def handle(self, command: ProcessOrderCommand) -> None:
        order = await self.order_repo.get_order(command.order_id)
        if not order:
            return

        if order.status == OrderStatus.PENDING:
            order.status = random.choice([OrderStatus.COMPLETED, OrderStatus.FAILED])

        async with self.uow:
            await self.order_repo.update_order(order)
            await self._mediator.publish(order.pull_events())
            await self.uow.commit()

            logger.info("Order processed", extra={"order": order})

        return None
