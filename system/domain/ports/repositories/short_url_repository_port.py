from abc import ABC, abstractmethod
from typing import List, Optional

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
    def query(
        self,
        hash_key: str,
        range_key: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ShortenedUrlEntity]:
        """
        Method that Returns a Short Url given a filter
        """
