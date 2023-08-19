from typing import Type

from system.application.dto.api.requests.url_request import UpdateShortUrlDTO
from system.application.dto.api.response.url_response import ShortUrlResponse
from system.domain.ports.repositories.use_case_port import RequestUseCase
from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)
from system.infrastructure.settings.container import Container


class UpdateShortUrlUseCase(RequestUseCase[UpdateShortUrlDTO, ShortUrlResponse]):
    def __init__(
        self,
        short_url_repository: Type[ShortUrlRepository] = Container.short_url_repository,
    ) -> None:
        self.short_url_repository = short_url_repository()

    def execute(
        self,
        payload: UpdateShortUrlDTO,
    ) -> ShortUrlResponse:
        raise Exception(payload)
