from typing import Type

from fastapi import status

from system.application.dto.api.response.url_response import ListAllShortUrlResponse
from system.domain.ports.repositories.use_case_port import RequestUseCaseWithoutPayload
from system.infrastructure.adapters.entrypoints.api.routes.admin.base_admin_short_url_view import (
    AdminShortUrlView,
)
from system.infrastructure.adapters.entrypoints.api.routes.base_route import (
    BaseRouterView,
)


class QueryUrlView(BaseRouterView, AdminShortUrlView):
    def __init__(
        self,
        query_use_case: Type[RequestUseCaseWithoutPayload],  # type: ignore[type-arg]
    ):
        super().__init__()
        self.query_use_case = query_use_case()
        self._add_to_router()

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self.query_short_url,
                status_code=status.HTTP_200_OK,
                response_model=ListAllShortUrlResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="List All Short URLs",
            )

    async def query_short_url(
        self,
    ) -> ListAllShortUrlResponse:
        return ListAllShortUrlResponse(
            response=self.query_use_case.execute(),
        )
