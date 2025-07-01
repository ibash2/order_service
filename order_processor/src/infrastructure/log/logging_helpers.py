from logging import Logger


class LoggingHelper:

    def __init__(self, logger: Logger) -> None:
        self.__logger = logger

    async def handle_logging_exception(self, handler: callable) -> None:
        try:
            await handler()
        except Exception as e:
            self.__logger.exception(e)
