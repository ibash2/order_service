from dataclasses import dataclass
import logging
from uuid import UUID

from application.common.command import Command
from application.common.command import CommandHandler
from application.common.interfaces.uow import UnitOfWork
from domain.user.entities.user import User
from application.user.interfaces.persistence.repo import UserRepo

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUserCommand(Command):
    login: str
    password: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, UUID]):
    uow: UnitOfWork
    user_repo: UserRepo

    async def handle(self, command: CreateUserCommand) -> UUID:
        user = User.create(command.login, command.password)

        async with self.uow:
            await self.user_repo.add_user(user)
            await self._mediator.publish(user.pull_events())
            await self.uow.commit()

            logger.info("User created", extra={"user": user})

        return user.id
