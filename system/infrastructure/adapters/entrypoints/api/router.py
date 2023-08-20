from fastapi.routing import APIRouter

from system.application.usecase.short_url.create_short_url_usecase import (
    CreateShortUrlUseCase,
)
from system.application.usecase.short_url.query_short_url_usecase import (
    QueryShortUrlUseCase,
)
from system.application.usecase.short_url.redirect_short_url_usecase import (
    RedirectQueryShortUrlUseCase,
)
from system.application.usecase.short_url.update_short_url_usecase import (
    UpdateShortUrlUseCase,
)
from system.infrastructure.adapters.entrypoints.api import monitoring
from system.infrastructure.adapters.entrypoints.api.routes.short_url_view import (
    ShortUrlView,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
short = ShortUrlView(
    redirect_use_case=RedirectQueryShortUrlUseCase,
    create_use_case=CreateShortUrlUseCase,
    update_use_case=UpdateShortUrlUseCase,
    query_use_case=QueryShortUrlUseCase,
)

api_router.include_router(short.router)
