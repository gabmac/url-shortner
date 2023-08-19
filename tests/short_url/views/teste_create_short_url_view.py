from freezegun import freeze_time
from tests.short_url.views.conftest import ShortUrlViewConfTest


class TestCreateShortUrlView(ShortUrlViewConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_create_usecase.target.execute.return_value = (
            self.short_url_dto_fixture.mock_create_enable_response
        )

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_create_usecase.target.execute.reset_mock()

    @freeze_time("2023-03-09T16:00:00")
    async def test_create_short_url(self) -> None:
        self.assertEqual(
            self.client.post(
                self.url_create,
                json=self.short_url_dto_fixture.mock_create_request,
            ),
            self.short_url_dto_fixture.mock_create_enable_response,
        )

        self.patch_short_create_usecase.target.execute.assert_called_once_with(
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity,
        )
