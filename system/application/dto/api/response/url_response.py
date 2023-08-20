from datetime import datetime
from typing import List

from pydantic import Field

from system.application.dto.base_dto import BaseDTO
from system.domain.enums.short_url_enum import ShortUrlStatusEnum


class ShortUrlResponse(BaseDTO):
    target_url: str = Field(description="Destination URL")
    short_url: str = Field(description="Short URL")
    created_at: datetime = Field(description="Created time in UTC")
    updated_at: datetime = Field(description="Last Update Time in UTC")
    status: ShortUrlStatusEnum = Field(description="Possible Short Url Status")


class ViewShortUrlResponse(BaseDTO):
    response: ShortUrlResponse


class ListAllShortUrlResponse(BaseDTO):
    response: List[ShortUrlResponse]
