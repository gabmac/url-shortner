from fastapi import APIRouter


class ShortUrlView:
    router = None

    def __init__(
        self,
        name: str = "short",
    ):
        self.name = name
        if self.router is None:
            self.router = APIRouter(
                prefix=f"/{name}",
                tags=[name],
            )
