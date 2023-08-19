import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from system.infrastructure.adapters.database.models.base_model import BaseModel
from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config
from system.infrastructure.settings.web_application import app


class BaseConfTest(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["DATABASE_TABLE"] = "shorturl"
        os.environ["ENVIRONMENT"] = "local"
        os.environ["ENDPOINT_URL"] = "http://localhost:8000"
        os.environ["AWS_ACCESS_KEY_ID"] = "teste"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "teste"
        os.environ["AWS_SESSION_TOKEN"] = "teste"
        os.environ["AWS_DEFAULT_REGION"] = "sa-east-1"
        cls.addClassCleanup(patch.stopall)

        super().setUpClass()


class BaseRepositoryConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not BaseModel.exists() and Config.ENVIRONMENT == Environments.LOCAL.value:
            BaseModel.create_table(
                read_capacity_units=500,
                write_capacity_units=500,
                wait=True,
            )


class BaseUseCaseConfTest(BaseConfTest):
    pass


class BaseRouteConfTest(BaseConfTest):
    fastapi_app = app

    @property
    def client(self) -> TestClient:
        """
        Fixture that creates client for requesting server.

        :param fastapi_app: the application.
        :yield: client for the app.
        """

        test_client = TestClient(
            app=self.fastapi_app,
            base_url="http://localhost:9857/api",
        )

        test_client.headers.update(
            {
                "Content-Type": "application/json",
            },
        )

        return test_client
