from abc import ABC, abstractmethod
from typing import Any, Dict

from system.domain.entities.url_entity import ShortenedUrlEntity


class ShortUrlRepositoryPort(ABC):
    @abstractmethod
    def upsert(
        self,
        short_url_entity: ShortenedUrlEntity,
    ) -> ShortenedUrlEntity:
        """
        Method that Upserts Short Url data on database
        """

    @abstractmethod
    def select(
        self,
        filter: Dict[str, Any] = {},
    ) -> ShortenedUrlEntity:
        """
        Method that Returns a Short Url given a filter
        """
