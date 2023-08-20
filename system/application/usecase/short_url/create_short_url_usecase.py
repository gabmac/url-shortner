import random
from datetime import datetime
from time import time
from typing import Type

from system.application.dto.api.requests.url_request import NewShortUrlRequest
from system.application.dto.api.response.url_response import ShortUrlResponse
from system.application.usecase.short_url.basic_behavior_usecase import (
    HTTPPrefixNeededUseCase,
)
from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.enums.short_url_enum import ShortUrlStatusEnum
from system.domain.ports.repositories.use_case_port import RequestUseCase
from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)
from system.infrastructure.settings.container import Container


class CreateShortUrlUseCase(
    RequestUseCase[NewShortUrlRequest, ShortUrlResponse],
    HTTPPrefixNeededUseCase,
):
    def __init__(
        self,
        short_url_repository: Type[ShortUrlRepository] = Container.short_url_repository,
    ) -> None:
        self.short_url_repository = short_url_repository()

    def execute(self, payload: NewShortUrlRequest) -> ShortUrlResponse:
        short_url_entity = ShortenedUrlEntity(
            target_url=self._https_prefix(target_url=payload.target_url),
            short_url=self._create_short_url(),
            status=ShortUrlStatusEnum.ENABLE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        save_url_entity = self.short_url_repository.upsert(
            short_url_entity=short_url_entity,
        )

        return ShortUrlResponse.model_validate(save_url_entity)

    def _create_short_url(self) -> str:
        hex_time = hex(int(time()))

        hex_list = list(hex_time)

        return "".join(random.sample(hex_list, len(hex_list)))
