from tests.conftest import BaseRepositoryConfTest
from tests.short_url.fixtures import ShortUrlModelFixture


class ShortUrlRepositoryConftest(BaseRepositoryConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.short_url_model_fixture = ShortUrlModelFixture()
