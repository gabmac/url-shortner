from typing import Type

from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

from system.application.usecase.short_url.exceptions.create_short_url_exception import (
    NoURLWasFoundError,
)
from system.domain.ports.repositories.use_case_port import RequestUseCaseWithoutBody
from system.infrastructure.adapters.entrypoints.api.routes.base_route import (
    BaseRouterView,
)
from system.infrastructure.adapters.entrypoints.api.routes.short_url.base_short_url_view import (
    ShortUrlView,
)


class RedirectUrlView(BaseRouterView, ShortUrlView):
    def __init__(
        self,
        redirect_use_case: Type[RequestUseCaseWithoutBody],  # type: ignore[type-arg]
    ):
        super().__init__()
        self.redirect_use_case = redirect_use_case()
        self._add_to_router()

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/{short_url}",
                self.redirect_short_url,
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                methods=["GET"],
                description="Redirect to Targe Url given a enable short url",
            )

    async def redirect_short_url(
        self,
        short_url: str,
    ) -> RedirectResponse:
        try:
            short_url_entity = self.redirect_use_case.execute(
                payload=short_url,
            )
        except NoURLWasFoundError as error:
            raise HTTPException(
                detail=error.message,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return RedirectResponse(
            url=short_url_entity.target_url,
        )
