from tests.conftest import BaseRepositoryConfTest
from tests.short_url.conftest import BaseShortUrlConfTest
from tests.short_url.fixtures import ShortUrlModelFixture


class ShortUrlRepositoryConftest(BaseShortUrlConfTest, BaseRepositoryConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.short_url_model_fixture = ShortUrlModelFixture()
