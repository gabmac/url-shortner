from tests.short_url.repository.conftest import ShortUrlRepositoryConftest

from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)


class SelectShortUrl(ShortUrlRepositoryConftest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.mock_short_url_enable_model = (
            cls.short_url_model_fixture.mock_short_url_enable_model
        )
        cls.mock_short_url_enable_model.save()
        cls.mock_short_url_enable_entity = (
            cls.short_url_model_fixture.entity.mock_short_url_enable_entity.model_copy()
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.mock_short_url_enable_model.delete()

    async def test_query_only_hash_key(self) -> None:
        self.assertEqual(
            ShortUrlRepository().query(
                hash_key="ROUTE",
            ),
            [self.mock_short_url_enable_entity],
        )

    async def test_query_hash_and_range_key(self) -> None:
        self.assertEqual(
            ShortUrlRepository().query(
                hash_key="ROUTE",
                range_key=self.mock_short_url_enable_entity.short_url,
            ),
            [self.mock_short_url_enable_entity],
        )

    async def test_query_hash_and_range_key_and_filter(self) -> None:
        self.assertEqual(
            ShortUrlRepository().query(
                hash_key="ROUTE",
                range_key=self.mock_short_url_enable_entity.short_url,
                status="ENABLE",
            ),
            [self.mock_short_url_enable_entity],
        )

    async def test_query_without_return(self) -> None:
        self.assertEqual(
            ShortUrlRepository().query(
                hash_key="ROUTE",
                range_key=self.mock_short_url_enable_entity.short_url,
                status="DISABLE",
            ),
            [],
        )
