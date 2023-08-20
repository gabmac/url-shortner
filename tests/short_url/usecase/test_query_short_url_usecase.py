from tests.short_url.usecase.conftest import ShortUrlUseCaseConfTest

from system.application.usecase.short_url.query_short_url_usecase import (
    QueryShortUrlUseCase,
)


class TestQueryShortUrlUseCase(ShortUrlUseCaseConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_use_case_repository.target.query.return_value = [
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity,
        ]

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_use_case_repository.target.query.reset_mock()

    async def test_query_all_short_url(self) -> None:
        self.assertEqual(
            QueryShortUrlUseCase().execute(),
            [self.short_url_dto_fixture.mock_create_enable_response],
        )

        self.patch_short_use_case_repository.target.query.assert_called_once_with(
            hash_key="ROUTE",
        )

    async def test_update_non_existent_short_url(self) -> None:
        self.patch_short_use_case_repository.target.query.return_value = []

        self.assertEqual(
            QueryShortUrlUseCase().execute(),
            [],
        )

        self.patch_short_use_case_repository.target.query.assert_called_once_with(
            hash_key="ROUTE",
        )
