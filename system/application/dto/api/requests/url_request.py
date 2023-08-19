from pydantic import Field

from system.application.dto.base_dto import BaseDTO
from system.application.enums.regex_validation_enums import RegexValidationEnum


class NewShortUrlRequest(BaseDTO):
    redirect_url: str = Field(regex=RegexValidationEnum.twitter_url_regex.value)
