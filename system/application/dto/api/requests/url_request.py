from typing import Optional

from pydantic import Field

from system.application.dto.base_dto import BaseDTO
from system.application.enums.regex_validation_enums import RegexValidationEnum
from system.domain.enums.short_url_enum import ShortUrlStatusEnum


class NewShortUrlRequest(BaseDTO):
    target_url: str = Field(pattern=RegexValidationEnum.twitter_url_regex.value)


class UpdateShortUrlRequest(BaseDTO):
    target_url: Optional[str] = Field(
        pattern=RegexValidationEnum.twitter_url_regex.value,
    )
    status: Optional[ShortUrlStatusEnum]


class UpdateShortUrlDTO(UpdateShortUrlRequest):
    short_url: str
