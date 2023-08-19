from tests.conftest import BaseConfTest
from tests.short_url.fixtures import ShortUrlEntityFixtures


class BaseShortUrlConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.short_url_entity_fixture = ShortUrlEntityFixtures()
