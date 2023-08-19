"""Application Settings"""
from typing import Any, Awaitable, Callable, Coroutine, List

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from system.infrastructure.adapters.entrypoints.api.router import api_router
from system.infrastructure.cross_cutting.middleware_logging import (
    RequestContextLogMiddleware,
)
from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config


class AppConfig:
    """Application Configurations"""

    def __init__(
        self,
        init_applications: List[Callable[[Any], Any]],
        context_logger: RequestContextLogMiddleware = RequestContextLogMiddleware(),
    ):
        self.init_applications = init_applications
        self.app = FastAPI(
            title="Short Url",
            description="Given a Twitter URL the application will create a short url",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc",
        )

        self.app.on_event("startup")(self.startup(self.init_applications, self.app))
        self.app.add_exception_handler(
            exc_class_or_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            handler=self.exception_handler,
        )
        self.context_logger = context_logger

    @staticmethod
    def startup(
        init_applications: List[Callable[[Any], Any]],
        app: FastAPI,
    ) -> Callable[[], Coroutine[Any, Any, None]]:
        """Startup Application"""

        async def _startup() -> None:
            for application in init_applications:
                application(app)

        return _startup

    def init_cors(self) -> None:
        """Initialize CORS"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    # pylint: disable=unused-argument
    async def exception_handler(request: Request, exc: Exception) -> None:
        # pylint: enable=unused-argument
        if Config.ENVIRONMENT != Environments.LOCAL.value:
            raise HTTPException(
                detail="Something fail",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def init_request_log(self) -> None:
        """Initalize ElasticLogger"""
        self.app.add_middleware(
            BaseHTTPMiddleware,
            dispatch=self.context_logger.dispatch,
        )

    def init_routes(self) -> None:
        """Intialize Routes"""
        self.app.include_router(api_router, prefix="/api")

    def start_application(self) -> FastAPI:
        """Start Application with Environment"""
        self.init_request_log()
        self.init_cors()
        self.init_routes()
        self.init_routes()
        return self.app


applications_init: List[Callable[[Any], Awaitable[Any]]] = []  # noqa: TAE002
app = AppConfig(applications_init).start_application()
