from typing import Any, Dict

from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.ports.repositories.short_url_repository_port import (
    ShortUrlRepositoryPort,
)


class ShortUrlRepository(ShortUrlRepositoryPort):
    def upsert(
        self,
        short_url_entity: ShortenedUrlEntity,
    ) -> ShortenedUrlEntity:
        """
        Method that Upserts Short Url data on database
        """
        raise Exception(short_url_entity)

    def select(
        self,
        filter: Dict[str, Any] = {},
    ) -> ShortenedUrlEntity:
        """
        Method that Returns a Short Url given a filter
        """
        raise Exception(filter)
