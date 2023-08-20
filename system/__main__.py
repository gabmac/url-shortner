"""Initialize Uvicorn."""
from logging.config import dictConfig

import uvicorn

from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config


def api() -> None:
    """Main funtion to initialize a fastapi application."""
    if Config.ENVIRONMENT == Environments.LOCAL.value:
        log_level = "debug"
        reload = True
    else:
        log_level = "info"
        reload = False

    dictConfig(Config.LOGGER.CONFIG)

    uvicorn.run(
        "system.infrastructure.settings.web_application:app",
        host="0.0.0.0",
        port=9000,
        reload=reload,
        factory=False,
        log_level=log_level,
    )


if __name__ == "__main__":
    api()
