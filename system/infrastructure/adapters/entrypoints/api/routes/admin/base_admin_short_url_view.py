from fastapi import APIRouter


class AdminShortUrlView:
    router = None

    def __init__(
        self,
        name: str = "admin",
    ):
        self.name = name
        if self.router is None:
            self.router = APIRouter(
                prefix=f"/{name}",
                tags=[name],
            )
