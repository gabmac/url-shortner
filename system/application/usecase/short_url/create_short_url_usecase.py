from datetime import datetime
from typing import Type

import ulid

from system.application.dto.api.requests.url_request import NewShortUrlRequest
from system.application.dto.api.response.url_response import NewShortUrlResponse
from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.enums.short_url_enum import ShortUrlStatusEnum
from system.domain.ports.repositories.use_case_port import RequestUseCase
from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)
from system.infrastructure.settings.container import Container


class CreateShortUrlUseCase(RequestUseCase[NewShortUrlRequest, NewShortUrlResponse]):
    def __init__(
        self,
        short_url_repository: Type[ShortUrlRepository] = Container.short_url_repository,
    ) -> None:
        self.short_url_repository = short_url_repository()

    def execute(self, payload: NewShortUrlRequest) -> NewShortUrlResponse:
        short_url_entity = ShortenedUrlEntity(
            target_url=payload.target_url,
            short_url=ulid.new().str,
            status=ShortUrlStatusEnum.ENABLE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        save_url_entity = self.short_url_repository.upsert(
            short_url_entity=short_url_entity,
        )

        return NewShortUrlResponse.model_validate(save_url_entity)
