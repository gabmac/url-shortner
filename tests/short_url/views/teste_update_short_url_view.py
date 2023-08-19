from fastapi import status
from freezegun import freeze_time
from tests.short_url.views.conftest import ShortUrlViewConfTest

from system.application.dto.api.requests.url_request import UpdateShortUrlDTO
from system.application.dto.api.response.url_response import ShortUrlResponse
from system.application.usecase.short_url.exceptions.create_short_url_exception import (
    NoURLWasFoundError,
)


class TestUpdateShortUrlView(ShortUrlViewConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_update_usecase.target.execute.return_value = (
            self.short_url_dto_fixture.mock_create_disable_response
        )

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_update_usecase.target.execute.reset_mock()

    @freeze_time("2023-03-09T16:00:00")
    async def test_update_short_url(self) -> None:
        response = self.client.patch(
            f"{self.url_update}/{self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url}",
            json=self.short_url_dto_fixture.mock_disable_request,
        )

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
        )
        self.assertEqual(
            ShortUrlResponse(**response.json()["response"]),
            self.short_url_dto_fixture.mock_create_disable_response,
        )

        self.patch_short_update_usecase.target.execute.assert_called_once_with(
            payload=UpdateShortUrlDTO(
                target_url=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.target_url,
                status=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.status,
                short_url=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url,
            ),
        )

    async def test_update_short_url_not_found(self) -> None:
        self.patch_short_update_usecase.target.execute.return_value = None
        self.patch_short_update_usecase.target.execute.side_effect = (
            NoURLWasFoundError()
        )

        response = self.client.patch(
            f"{self.url_update}/{self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url}",
            json=self.short_url_dto_fixture.mock_disable_request,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.patch_short_update_usecase.target.execute.assert_called_once_with(
            payload=UpdateShortUrlDTO(
                target_url=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.target_url,
                status=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.status,
                short_url=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url,
            ),
        )
