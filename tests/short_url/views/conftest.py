import random
from unittest.mock import patch

from tests.conftest import BaseviewConfTest
from tests.short_url.conftest import BaseShortUrlConfTest
from tests.short_url.fixtures import ShortRequestDTOFixture

from system.application.usecase.short_url.create_short_url_usecase import (
    CreateShortUrlUseCase,
)
from system.application.usecase.short_url.redirect_short_url_usecase import (
    RedirectQueryShortUrlUseCase,
)
from system.application.usecase.short_url.update_short_url_usecase import (
    UpdateShortUrlUseCase,
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
        cls.patch_short_update_usecase = patch.object(
            UpdateShortUrlUseCase,
            "execute",
        )
        cls.patch_short_update_usecase.start()

        cls.patch_short_redirect_usecase = patch.object(
            RedirectQueryShortUrlUseCase,
            "execute",
        )
        cls.patch_short_redirect_usecase.start()

        cls.url_create = cls.fastapi_app.url_path_for("create_short_url")
        cls.url_update = "/api/short/admin"
        cls.url_redirect = "/api/short"

        cls.patch_random = patch.object(
            random,
            "sample",
        )
        cls.patch_random.start()

        cls.patch_random.target.sample.return_value = [
            cls.short_url_dto_fixture.entity.short_url,
        ]

        super().setUpClass()
