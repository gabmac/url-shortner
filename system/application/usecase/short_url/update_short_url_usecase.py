from typing import Type

from system.application.dto.api.requests.url_request import UpdateShortUrlDTO
from system.application.dto.api.response.url_response import ShortUrlResponse
from system.application.usecase.short_url.exceptions.create_short_url_exception import (
    NoURLWasFoundError,
)
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
        try:
            short_url = self.short_url_repository.query(
                hash_key="ROUTE",
                range_key=payload.short_url,
            )[0]

            short_url.status = payload.status
        except IndexError:
            raise NoURLWasFoundError()

        return ShortUrlResponse.model_validate(
            self.short_url_repository.upsert(
                short_url_entity=short_url,
            ),
        )
