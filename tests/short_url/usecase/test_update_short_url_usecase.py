import copy

from tests.short_url.usecase.conftest import ShortUrlUseCaseConfTest

from system.application.dto.api.requests.url_request import UpdateShortUrlDTO
from system.application.usecase.short_url.update_short_url_usecase import (
    UpdateShortUrlUseCase,
)


class TestUpdateShortUrlUseCase(ShortUrlUseCaseConfTest):
    def setUp(self) -> None:
        super().setUp()
        self.patch_short_use_case_repository.target.query.return_value = [
            self.short_url_dto_fixture.entity.mock_short_url_enable_entity,
        ]
        self.patch_short_use_case_repository.target.upsert.return_value = (
            self.short_url_dto_fixture.entity.mock_short_url_disable_entity
        )
        self.patch_short_use_case_repository.target.upsert.side_effect = None

        self.short_url_dto_fixture_change_target = copy.deepcopy(
            self.short_url_dto_fixture,
        )
        self.short_url_dto_fixture_change_target.target_url = (
            "https://twitter.com/teste123"
        )

    def tearDown(self) -> None:
        super().tearDown()
        self.patch_short_use_case_repository.target.upsert.reset_mock()
        self.patch_short_use_case_repository.target.query.reset_mock()

    async def test_change_status_short_url(self) -> None:
        self.assertEqual(
            UpdateShortUrlUseCase().execute(
                payload=UpdateShortUrlDTO(
                    target_url=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.target_url,
                    status=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.status,
                    short_url=self.short_url_dto_fixture.entity.mock_short_url_disable_entity.short_url,
                ),
            ),
            self.short_url_dto_fixture.mock_create_disable_response,
        )

        self.patch_short_use_case_repository.target.query.assert_called_once_with(
            hash_key="ROUTE",
            range_key=self.short_url_dto_fixture.entity.mock_short_url_enable_entity.short_url,
        )

        self.patch_short_use_case_repository.target.upsert.assert_called_once_with(
            short_url_entity=self.short_url_dto_fixture.entity.mock_short_url_disable_entity,
        )

    async def test_change_target_url(self) -> None:
        self.patch_short_use_case_repository.target.upsert.return_value = (
            self.short_url_dto_fixture_change_target.entity.mock_short_url_enable_entity
        )

        self.assertEqual(
            UpdateShortUrlUseCase().execute(
                payload=UpdateShortUrlDTO(
                    target_url=self.short_url_dto_fixture_change_target.entity.mock_short_url_enable_entity.target_url,
                    status=self.short_url_dto_fixture_change_target.entity.mock_short_url_enable_entity.status,
                    short_url=self.short_url_dto_fixture_change_target.entity.mock_short_url_enable_entity.short_url,
                ),
            ),
            self.short_url_dto_fixture_change_target.mock_create_enable_response,
        )

        self.patch_short_use_case_repository.target.query.assert_called_once_with(
            hash_key="ROUTE",
            range_key=self.short_url_dto_fixture_change_target.entity.mock_short_url_enable_entity.short_url,
        )

        self.patch_short_use_case_repository.target.upsert.assert_called_once_with(
            short_url_entity=self.short_url_dto_fixture.entity.mock_short_url_enable_entity,
        )

    async def test_update_non_existent_short_url(self) -> None:
        raise Exception()
