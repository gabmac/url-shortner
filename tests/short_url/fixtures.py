from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.enums.short_url_enum import ShortUrlStatusEnum


class ShortUrlEntityFixtures:
    def __init__(
        self,
        redirect_url: str = "https://google.com.br",
        short_url: str = "ShOrT",
    ) -> None:
        self.redirect_url = redirect_url
        self.short_url = short_url

    @property
    def mock_short_url_enable(self) -> ShortenedUrlEntity:
        return ShortenedUrlEntity(
            redirect_url=self.redirect_url,
            short_url=self.short_url,
            status=ShortUrlStatusEnum.ENABLE,
        )

    @property
    def mock_short_url_disable(self) -> ShortenedUrlEntity:
        short_url = self.mock_short_url_enable.model_copy()
        short_url.status = ShortUrlStatusEnum.DISABLE

        return short_url
