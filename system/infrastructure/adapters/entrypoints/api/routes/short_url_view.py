from typing import Type

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from system.application.dto.api.requests.url_request import (
    NewShortUrlRequest,
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
            description="Create Short Url",
        )

        self.router.add_api_route(
            "/admin/{short_url}",
            self.update_short_url,
            status_code=status.HTTP_200_OK,
            response_model=ViewShortUrlResponse,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["PATCH"],
            description="Update Short Url",
        )

        self.router.add_api_route(
            "/{short_url}",
            self.redirect_short_url,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            methods=["GET"],
            description="Redirect to Targe Url given a enable short url",
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
