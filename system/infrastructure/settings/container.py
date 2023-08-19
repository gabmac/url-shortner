from system.infrastructure.adapters.database.repositories.short_url_repository import (
    ShortUrlRepository,
)


class Container:
    short_url_repository = ShortUrlRepository
