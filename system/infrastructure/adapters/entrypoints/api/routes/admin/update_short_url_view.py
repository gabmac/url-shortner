from typing import Type

from fastapi import HTTPException, status

from system.application.dto.api.requests.url_request import (
    UpdateShortUrlDTO,
    UpdateShortUrlRequest,
)
from system.application.dto.api.response.url_response import (
    ShortUrlResponse,
    ViewShortUrlResponse,
)
from system.application.usecase.short_url.exceptions.create_short_url_exception import (
    NoURLWasFoundError,
)
from system.domain.ports.repositories.use_case_port import RequestUseCase
from system.infrastructure.adapters.entrypoints.api.routes.admin.base_admin_short_url_view import (
    AdminShortUrlView,
)
from system.infrastructure.adapters.entrypoints.api.routes.base_route import (
    BaseRouterView,
)


class UpdateUrlView(BaseRouterView, AdminShortUrlView):
    def __init__(
        self,
        update_use_case: Type[RequestUseCase],  # type: ignore[type-arg]
    ):
        super().__init__()
        self.update_use_case = update_use_case()
        self._add_to_router()

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/{short_url}",
                self.update_short_url,
                status_code=status.HTTP_200_OK,
                response_model=ViewShortUrlResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["PATCH"],
                description="Update Short Url",
            )

    async def update_short_url(
        self,
        short_url: str,
        payload: UpdateShortUrlRequest,
    ) -> ViewShortUrlResponse:
        try:
            return ViewShortUrlResponse(
                response=ShortUrlResponse.model_validate(
                    self.update_use_case.execute(
                        payload=UpdateShortUrlDTO(
                            short_url=short_url,
                            target_url=payload.target_url,
                            status=payload.status,
                        ),
                    ),
                ),
            )
        except NoURLWasFoundError as error:
            raise HTTPException(
                detail=error.message,
                status_code=status.HTTP_404_NOT_FOUND,
            )
