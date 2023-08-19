from enum import Enum


class RegexValidationEnum(Enum):
    twitter_url_regex = (
        r"^(?:https?:\/\/)?(?:www\.)?twitter\.com\/[A-Za-z0-9_\/\?=&%-]+$"
    )
