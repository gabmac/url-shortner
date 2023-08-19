from unittest.mock import patch

import ulid
from tests.conftest import BaseviewConfTest
from tests.short_url.conftest import BaseShortUrlConfTest
from tests.short_url.fixtures import ShortRequestDTOFixture

from system.application.usecase.short_url.create_short_url_usecase import (
    CreateShortUrlUseCase,
)


class ShortUrlViewConfTest(BaseShortUrlConfTest, BaseviewConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.short_url_dto_fixture = ShortRequestDTOFixture()
        cls.patch_short_create_usecase = patch.object(
            CreateShortUrlUseCase,
            "execute",
        )
        cls.patch_short_create_usecase.start()

        cls.url_create = cls.fastapi_app.url_path_for("create_short_url")

        cls.patch_ulid = patch.object(
            ulid,
            "new",
        )
        cls.patch_ulid.start()

        cls.patch_ulid.target.new.return_value = (
            cls.short_url_dto_fixture.entity.short_url
        )

        super().setUpClass()
