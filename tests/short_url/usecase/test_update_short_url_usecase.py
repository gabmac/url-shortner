from tests.short_url.usecase.conftest import ShortUrlUseCaseConfTest


class TestUpdateShortUrlUseCase(ShortUrlUseCaseConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_use_case_repository.target.upsert.return_value = (
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity
        )
        self.patch_short_use_case_repository.target.upsert.side_effect = None

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_use_case_repository.target.upsert.reset_mock()

    async def test_update_short_url(self) -> None:
        raise Exception()

    async def test_update_non_existent_short_url(self) -> None:
        raise Exception()
