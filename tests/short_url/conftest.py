from tests.conftest import BaseUseCaseConfTest
from tests.short_url.fixtures import ShortUrlEntityFixtures


class BaseShortUrlConfTest(BaseUseCaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.short_url_entity_fixture = ShortUrlEntityFixtures()
