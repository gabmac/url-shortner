from fastapi import status
from freezegun import freeze_time
from tests.short_url.views.conftest import ShortUrlViewConfTest

from system.application.dto.api.response.url_response import ShortUrlResponse


class QueryShortUrlView(ShortUrlViewConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_query_usecase.target.execute.return_value = [
            self.short_url_dto_fixture.mock_create_enable_response,
        ]

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_query_usecase.target.execute.reset_mock()

    @freeze_time("2023-03-09T16:00:00")
    async def test_query_short_url(self) -> None:
        response = self.client.get(
            f"{self.url_query}",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            [
                ShortUrlResponse(**response_value)
                for response_value in response.json()["response"]
            ],
            [self.short_url_dto_fixture.mock_create_enable_response],
        )

        self.patch_short_query_usecase.target.execute.assert_called_once()

    async def test_query_short_url_not_found(self) -> None:
        self.patch_short_query_usecase.target.execute.return_value = []

        response = self.client.get(
            f"{self.url_query}",
        )

        self.assertEqual(
            response.json()["response"],
            [],
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.patch_short_query_usecase.target.execute.assert_called_once()
