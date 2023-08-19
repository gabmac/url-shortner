from datetime import datetime

from system.application.dto.base_dto import BaseDTO
from system.domain.enums.short_url_enum import ShortUrlStatusEnum


class ShortUrlResponse(BaseDTO):
    target_url: str
    short_url: str
    created_at: datetime
    updated_at: datetime
    status: ShortUrlStatusEnum
