from datetime import datetime

from pydantic import Field

from system.domain.entities.base_entity import BaseEntity
from system.domain.enums.short_url_enum import ShortUrlStatusEnum


class ShortenedUrlEntity(BaseEntity):
    target_url: str
    short_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: ShortUrlStatusEnum
