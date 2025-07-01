import logging

from fastapi import FastAPI

from infrastructure.log.config import LoggingConfig
from infrastructure.log.main import configure_logging
from presentation.api.main import init_api


logger = logging.getLogger(__name__)


def main() -> FastAPI:
    configure_logging(LoggingConfig(render_json_logs=False, level="INFO"))
    logger.info("Launch app")
    app = init_api()
    return app


# if __name__ == "__main__":
#     asyncio.run(main())
