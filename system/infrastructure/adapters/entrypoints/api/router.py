from fastapi.routing import APIRouter

from system.infrastructure.adapters.entrypoints.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
