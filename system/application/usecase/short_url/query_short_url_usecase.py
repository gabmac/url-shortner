from typing import List, Type

from system.application.dto.api.response.url_response import ShortUrlResponse
from system.domain.ports.repositories.use_case_port import RequestUseCaseWithoutPayload
from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)
from system.infrastructure.settings.container import Container


class QueryShortUrlUseCase(RequestUseCaseWithoutPayload[List[ShortUrlResponse]]):
    def __init__(
        self,
        short_url_repository: Type[ShortUrlRepository] = Container.short_url_repository,
    ) -> None:
        self.short_url_repository = short_url_repository()

    def execute(self) -> List[ShortUrlResponse]:
        short_urls = self.short_url_repository.query(
            hash_key="ROUTE",
        )

        return [ShortUrlResponse.model_validate(url) for url in short_urls]
