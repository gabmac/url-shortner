from pydantic import Field

from system.application.dto.base_dto import BaseDTO
from system.application.enums.regex_validation_enums import RegexValidationEnum


class NewShortUrlRequest(BaseDTO):
    target_url: str = Field(pattern=RegexValidationEnum.twitter_url_regex.value)
