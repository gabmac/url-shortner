from tests.short_url.repository.conftest import ShortUrlRepositoryConftest

from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)


class UpsertShortUrl(ShortUrlRepositoryConftest):
    def tearDown(self) -> None:
        super().tearDown()
        self.short_url_model_fixture.mock_short_url_enable_model.delete()

    async def test_update_short_url(self):
        self.short_url_model_fixture.mock_short_url_enable_model.save()
        self.assertEqual(
            ShortUrlRepository.upsert(
                short_url_entity=self.short_url_model_fixture.entity.mock_short_url_disable_entity,
            ),
            self.short_url_model_fixture.entity.mock_short_url_disable_entity,
        )

    async def test_insert_short_url(self):
        self.assertEqual(
            ShortUrlRepository.upsert(
                short_url_entity=self.short_url_model_fixture.entity.mock_short_url_enable_entity,
            ),
            self.short_url_model_fixture.entity.mock_short_url_enable_entity,
        )
