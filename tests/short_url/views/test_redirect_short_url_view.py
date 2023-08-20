from fastapi import status
from freezegun import freeze_time
from tests.short_url.views.conftest import ShortUrlViewConfTest

from system.application.usecase.short_url.exceptions.create_short_url_exception import (
    NoURLWasFoundError,
)


class TestRedirectShortUrlView(ShortUrlViewConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_redirect_usecase.target.execute.return_value = (
            self.short_url_dto_fixture.mock_create_enable_response
        )

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_redirect_usecase.target.execute.reset_mock()

    @freeze_time("2023-03-09T16:00:00")
    async def test_redirect_short_url(self) -> None:
        response = self.client.get(
            f"{self.url_redirect}/{self.short_url_dto_fixture.entity.mock_short_url_enable_entity.short_url}",
        )

        self.assertEqual(
            response.url.__str__(),
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity.target_url,
        )

        self.patch_short_redirect_usecase.target.execute.assert_called_once_with(
            payload=self.short_url_dto_fixture.entity.mock_short_url_enable_entity.short_url,
        )

    async def test_redirect_short_url_not_found(self) -> None:
        self.patch_short_redirect_usecase.target.execute.return_value = None
        self.patch_short_redirect_usecase.target.execute.side_effect = (
            NoURLWasFoundError()
        )

        response = self.client.get(
            f"{self.url_redirect}/{self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url}",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.patch_short_redirect_usecase.target.execute.assert_called_once_with(
            payload=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url,
        )
