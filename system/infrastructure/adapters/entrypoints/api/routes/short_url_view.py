from typing import Type

from fastapi import APIRouter, status

from system.application.dto.api.requests.url_request import NewShortUrlRequest
from system.application.dto.api.response.url_response import (
    ShortUrlResponse,
    ViewShortUrlResponse,
)
from system.domain.ports.repositories.use_case_port import (
    RequestUseCase,
    RequestUseCaseWithoutBody,
)


class ShortUrlView:
    def __init__(
        self,
        redirect_use_case: Type[RequestUseCaseWithoutBody],  # type: ignore[type-arg]
        create_use_case: Type[RequestUseCase],  # type: ignore[type-arg]
        update_use_case: Type[RequestUseCase],  # type: ignore[type-arg]
        name: str = "short",
    ):
        self.name = name
        self.router = APIRouter(
            prefix=f"/{name}",
            tags=[name],
        )
        self.redirect_use_case = redirect_use_case()
        self.create_use_case = create_use_case()
        self.update_use_case = update_use_case()

        self.router.add_api_route(
            "/admin",
            self.create_short_url,
            status_code=status.HTTP_201_CREATED,
            response_model=ViewShortUrlResponse,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["POST"],
        )

    async def create_short_url(
        self,
        payload: NewShortUrlRequest,
    ) -> ViewShortUrlResponse:
        return ViewShortUrlResponse(
            response=ShortUrlResponse.model_validate(
                self.create_use_case.execute(
                    payload=payload,
                ),
            ),
        )
