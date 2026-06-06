from fastapi import APIRouter

from .routers.health import router as health_router

ROUTERS: list[APIRouter] = [
    health_router,
]

router = APIRouter(prefix='/ws')

for r in ROUTERS:
    router.include_router(r)
