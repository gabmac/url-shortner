from tests.short_url.usecase.conftest import ShortUrlUseCaseConfTest

from system.application.usecase.short_url.exceptions.create_short_url_exception import (
    NoURLWasFoundError,
)
from system.application.usecase.short_url.redirect_short_url_usecase import (
    RedirectQueryShortUrlUseCase,
)


class TestRedirectQueryShortUrlUseCase(ShortUrlUseCaseConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_use_case_repository.target.query.return_value = [
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity,
        ]

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_use_case_repository.target.query.reset_mock()

    async def test_redirect_short_url(self) -> None:
        self.assertEqual(
            RedirectQueryShortUrlUseCase().execute(
                payload=self.short_url_dto_fixture.mock_create_enable_response.short_url,
            ),
            self.short_url_dto_fixture.mock_create_enable_response,
        )

        self.patch_short_use_case_repository.target.query.assert_called_once_with(
            hash_key="ROUTE",
            range_key=self.short_url_dto_fixture.entity.mock_short_url_enable_entity.short_url,
            status="ENABLE",
        )

    async def test_update_non_existent_short_url(self) -> None:
        self.patch_short_use_case_repository.target.query.return_value = []
        short_url = "234567f"

        with self.assertRaises(NoURLWasFoundError) as error:
            RedirectQueryShortUrlUseCase().execute(
                payload=self.short_url_dto_fixture.mock_create_enable_response.short_url,
            )

            self.assertEqual(
                error.message,
                NoURLWasFoundError().message,
            )

            self.patch_short_use_case_repository.target.query.assert_called_once_with(
                hash_key="ROUTE",
                range_key=short_url,
            )

            self.patch_short_use_case_repository.target.upsert.assert_not_called()
