"""Initialize Uvicorn."""
import uvicorn

from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config


def api() -> None:
    """Main funtion to initialize a fastapi application."""
    if Config.ENVIRONMENT == Environments.LOCAL.value:
        debug = True
        log_level = "debug"
        reload = True
    else:
        debug = False
        log_level = "info"
        reload = False

    uvicorn.run(
        "system.infrastructure.settings.web_application:app",
        host="0.0.0.0",
        port=9000,
        reload=reload,
        factory=False,
        debug=debug,
        log_level=log_level,
    )


if __name__ == "__main__":
    api()
