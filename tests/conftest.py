from unittest import IsolatedAsyncioTestCase

from system.infrastructure.adapters.models.base_model import BaseModel


class BaseConftest(IsolatedAsyncioTestCase):
    pass


class BaseRepositoryConfTest(BaseConftest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not BaseModel.exists():
            BaseModel.create_table()
