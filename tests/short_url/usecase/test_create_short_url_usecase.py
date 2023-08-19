from freezegun import freeze_time
from tests.short_url.usecase.conftest import ShortUrlUseCaseConfTest

from system.application.usecase.short_url.create_short_url_usecase import (
    CreateShortUrlUseCase,
)


class TestCreateShortUrlUseCase(ShortUrlUseCaseConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_use_case_repository.target.upsert.return_value = (
            self.short_url_entity_fixture.mock_short_url_enable_entity
        )
        self.patch_short_use_case_repository.target.upsert.side_effect = None

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_use_case_repository.target.upsert.return_value.reset_mock()

    @freeze_time("2023-03-09T16:00:00")
    async def test_create_short_url(self) -> None:
        self.assertEqual(
            CreateShortUrlUseCase().execute(
                payload=self.short_url_dto_fixture.mock_create_request,
            ),
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity,
        )

        self.patch_short_use_case_repository.target.upsert.assert_called_once_with(
            short_url_entity=self.short_url_entity_fixture.mock_short_url_enable_entity,
        )
