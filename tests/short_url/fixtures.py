from datetime import datetime

from system.application.dto.api.requests.url_request import (
    NewShortUrlRequest,
    UpdateShortUrlRequest,
)
from system.application.dto.api.response.url_response import ShortUrlResponse
from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.enums.short_url_enum import ShortUrlStatusEnum
from system.infrastructure.adapters.database.models.short_url_model import ShortUrlModel


class ShortUrlEntityFixtures:
    def __init__(
        self,
        target_url: str = "https://twitter.com/home",
        short_url: str = "x24eb5601f",
    ) -> None:
        self.target_url = target_url
        self.short_url = short_url

    @property
    def mock_short_url_enable_entity(self) -> ShortenedUrlEntity:
        return ShortenedUrlEntity(
            target_url=self.target_url,
            short_url=self.short_url,
            status=ShortUrlStatusEnum.ENABLE,
            created_at=datetime(2023, 3, 9, 16, 0, 0, 0),
            updated_at=datetime(2023, 3, 9, 16, 0, 0, 0),
        )

    @property
    def mock_short_url_disable_entity(self) -> ShortenedUrlEntity:
        short_url = self.mock_short_url_enable_entity.model_copy()
        short_url.status = ShortUrlStatusEnum.DISABLE

        return short_url


class ShortUrlModelFixture:
    def __init__(
        self,
        target_url: str = "https://twitter.com/home",
        short_url: str = "x24eb5601f",
    ) -> None:
        self.target_url = target_url
        self.short_url = short_url
        self.entity = ShortUrlEntityFixtures(
            target_url=self.target_url,
            short_url=self.short_url,
        )

    @property
    def mock_short_url_enable_model(self) -> ShortUrlModel:
        return ShortUrlModel(
            **self.entity.mock_short_url_enable_entity.model_dump(),
            populate_all_fields=True,
        )

    @property
    def mock_short_url_disable_model(self) -> ShortenedUrlEntity:
        return ShortUrlModel(
            **self.entity.mock_short_url_disable_entity.model_dump(),
            populate_all_fields=True,
        )


class ShortRequestDTOFixture:
    def __init__(
        self,
        target_url: str = "https://twitter.com/home",
        short_url: str = "x24eb5601f",
    ) -> None:
        self.target_url = target_url
        self.short_url = short_url

    @property
    def entity(self) -> ShortUrlEntityFixtures:
        return ShortUrlEntityFixtures(
            target_url=self.target_url,
            short_url=self.short_url,
        )

    @property
    def mock_create_request(self) -> NewShortUrlRequest:
        return NewShortUrlRequest(
            target_url=self.entity.target_url,
        )

    @property
    def mock_disable_request(self) -> NewShortUrlRequest:
        return UpdateShortUrlRequest(
            target_url=self.entity.target_url,
            status="DISABLE",
        )

    @property
    def mock_create_enable_response(self) -> ShortUrlResponse:
        return ShortUrlResponse(
            **self.entity.mock_short_url_enable_entity.model_dump(),
        )

    @property
    def mock_create_disable_response(self) -> ShortUrlResponse:
        return ShortUrlResponse(
            **self.entity.mock_short_url_disable_entity.model_dump(),
        )
