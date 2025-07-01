from dataclasses import dataclass

from application.common.exceptions import ApplicationError

@dataclass(eq=False)
class UserNotExistError(ApplicationError):

    @property
    def message(self) -> str:
        return 'A user doesn\'t exist'
