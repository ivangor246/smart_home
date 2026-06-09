from fastapi import APIRouter

from .routers.bus import router as bus_router
from .routers.camera import router as camera_router
from .routers.health import router as health_router

ROUTERS: list[APIRouter] = [
    bus_router,
    camera_router,
    health_router,
]

router = APIRouter(prefix='/ws')

for r in ROUTERS:
    router.include_router(r)
