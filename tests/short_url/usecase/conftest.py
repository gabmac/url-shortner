from unittest.mock import DEFAULT, patch

from tests.short_url.conftest import BaseShortUrlConfTest
from tests.short_url.fixtures import ShortRequestDTOFixture

from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)


class ShortUrlUseCaseConfTest(BaseShortUrlConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.short_url_dto_fixture = ShortRequestDTOFixture()
        cls.patch_short_use_case_repository = patch(
            ShortUrlRepository,
            upsert=DEFAULT,
            query=DEFAULT,
        )
