from tests.conftest import BaseRepositoryConfTest
from tests.short_url.fixtures import ShortUrlEntityFixtures


class BaseShortUrlConfTest(BaseRepositoryConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.short_url_entity_fixture = ShortUrlEntityFixtures()
