from typing import Type

from fastapi import status

from system.application.dto.api.requests.url_request import NewShortUrlRequest
from system.application.dto.api.response.url_response import (
    ShortUrlResponse,
    ViewShortUrlResponse,
)
from system.domain.ports.repositories.use_case_port import RequestUseCase
from system.infrastructure.adapters.entrypoints.api.routes.admin.base_admin_short_url_view import (
    AdminShortUrlView,
)
from system.infrastructure.adapters.entrypoints.api.routes.base_route import (
    BaseRouterView,
)


class CreateUrlView(BaseRouterView, AdminShortUrlView):
    def __init__(
        self,
        create_use_case: Type[RequestUseCase],  # type: ignore[type-arg]
    ):
        super().__init__()
        self.create_use_case = create_use_case()
        self._add_to_router()

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self.create_short_url,
                status_code=status.HTTP_201_CREATED,
                response_model=ViewShortUrlResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["POST"],
                description="Create Short Url",
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
