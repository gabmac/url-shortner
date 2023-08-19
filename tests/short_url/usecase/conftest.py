from unittest.mock import DEFAULT, patch

from tests.short_url.conftest import BaseShortUrlConfTest
from tests.short_url.fixtures import ShortRequestDTOFixture


class ShortUrlUseCaseConfTest(BaseShortUrlConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.short_url_dto_fixture = ShortRequestDTOFixture()
        cls.patch_short_use_case_repository = patch.multiple(
            "system.infrastructure.adapters.database.repositories.short_url_repository.ShortUrlRepository",
            upsert=DEFAULT,
            query=DEFAULT,
        )
        cls.patch_short_use_case_repository.start()
        super().setUpClass()
