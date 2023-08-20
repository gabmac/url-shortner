from typing import Optional

from pydantic import Field, constr

from system.application.dto.base_dto import BaseDTO
from system.application.enums.regex_validation_enums import RegexValidationEnum
from system.domain.enums.short_url_enum import ShortUrlStatusEnum


class NewShortUrlRequest(BaseDTO):
    target_url: str = Field(
        pattern=RegexValidationEnum.twitter_url_regex.value,
        description="Destination URL to which the shortened URL will redirect",
    )


class UpdateShortUrlRequest(BaseDTO):
    target_url: Optional[  # type: ignore[valid-type]
        constr(pattern=RegexValidationEnum.twitter_url_regex.value)
    ] = Field(
        default=None,
        description="Destination URL to which the shortened URL will redirect",
    )
    status: Optional[ShortUrlStatusEnum] = Field(
        default=None,
        description="Short Url Status",
    )


class UpdateShortUrlDTO(UpdateShortUrlRequest):
    short_url: str = Field(description="Short Url Status")
