from enum import Enum


class RegexValidationEnum(Enum):
    twitter_url_regex = (
        r"^(?:http(?:s?)?:\/\/)?(?:www\.)?twitter\.com(?:\/[A-Za-z0-9_\/\?=&%-]+$)?"
    )
