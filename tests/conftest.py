from unittest import IsolatedAsyncioTestCase

from system.infrastructure.adapters.models.base_model import BaseModel


class BaseConfTest(IsolatedAsyncioTestCase):
    pass


class BaseRepositoryConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not BaseModel.exists():
            BaseModel.create_table()
