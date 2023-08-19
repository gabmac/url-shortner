from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.enums.short_url_enum import ShortUrlStatusEnum
from system.infrastructure.adapters.database.models.short_url_model import ShortUrlModel


class ShortUrlEntityFixtures:
    def __init__(
        self,
        redirect_url: str = "https://google.com.br",
        short_url: str = "ShOrT",
    ) -> None:
        self.redirect_url = redirect_url
        self.short_url = short_url

    @property
    def mock_short_url_enable_entity(self) -> ShortenedUrlEntity:
        return ShortenedUrlEntity(
            redirect_url=self.redirect_url,
            short_url=self.short_url,
            status=ShortUrlStatusEnum.ENABLE,
        )

    @property
    def mock_short_url_disable_entity(self) -> ShortenedUrlEntity:
        short_url = self.mock_short_url_enable_entity.model_copy()
        short_url.status = ShortUrlStatusEnum.DISABLE

        return short_url


class ShortUrlModelFixture:
    def __init__(
        self,
        redirect_url: str = "https://google.com.br",
        short_url: str = "ShOrT",
    ) -> None:
        self.redirect_url = redirect_url
        self.short_url = short_url
        self.entity = ShortUrlEntityFixtures(
            redirect_url=self.redirect_url,
            short_url=self.short_url,
        )

    @property
    def mock_short_url_enable_model(self) -> ShortUrlModel:
        return ShortUrlModel(**self.entity.mock_short_url_enable_entity.model_dump())

    @property
    def mock_short_url_disable_model(self) -> ShortenedUrlEntity:
        return ShortUrlModel(**self.entity.mock_short_url_disable_entity.model_dump())
