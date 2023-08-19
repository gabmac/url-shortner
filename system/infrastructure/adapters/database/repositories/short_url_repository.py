from typing import List, Optional

from system.domain.entities.url_entity import ShortenedUrlEntity
from system.domain.ports.repositories.short_url_repository_port import (
    ShortUrlRepositoryPort,
)
from system.infrastructure.adapters.database.models.short_url_model import ShortUrlModel


class ShortUrlRepository(ShortUrlRepositoryPort):
    def upsert(
        self,
        short_url_entity: ShortenedUrlEntity,
    ) -> ShortenedUrlEntity:
        """
        Method that Upserts Short Url data on database
        """
        model = ShortUrlModel(**short_url_entity.model_dump(), populate_all_fields=True)

        model.save()

        return ShortenedUrlEntity.model_validate(model)

    def query(
        self,
        hash_key: str,
        range_key: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ShortenedUrlEntity]:
        """
        Method that Returns a Short Url given a filter
        """

        range_key_condition = (
            ShortUrlModel.sk == range_key if range_key is not None else None
        )
        status_condition = (
            ShortUrlModel.status == status if status is not None else None
        )
        entity_list = []

        for url in ShortUrlModel.query(
            hash_key=hash_key,
            range_key_condition=range_key_condition,
            filter_condition=status_condition,
        ):
            entity_list.append(ShortenedUrlEntity.model_validate(url))

        return entity_list
