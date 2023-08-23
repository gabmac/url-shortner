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
from system.infrastructure.adapters.entrypoints.api.routes.admin.create_short_url_view import (
    CreateUrlView,
)
from system.infrastructure.adapters.entrypoints.api.routes.admin.query_short_url_view import (
    QueryUrlView,
)
from system.infrastructure.adapters.entrypoints.api.routes.admin.update_short_url_view import (
    UpdateUrlView,
)
from system.infrastructure.adapters.entrypoints.api.routes.short_url.redirect_short_url import (
    RedirectUrlView,
)

api_router = APIRouter(prefix="/api")
api_router.include_router(monitoring.router)

redirect = RedirectUrlView(
    redirect_use_case=RedirectQueryShortUrlUseCase,
)
update = UpdateUrlView(
    update_use_case=UpdateShortUrlUseCase,
)
query = QueryUrlView(
    query_use_case=QueryShortUrlUseCase,
)

create = CreateUrlView(
    create_use_case=CreateShortUrlUseCase,
)

api_router.include_router(redirect.router)  # type: ignore[arg-type]
api_router.include_router(update.router)  # type: ignore[arg-type]
api_router.include_router(query.router)  # type: ignore[arg-type]
api_router.include_router(create.router)  # type: ignore[arg-type]
