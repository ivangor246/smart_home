from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import root_router
from app.core import config
from app.ws import ws_root_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='smart_home',
        debug=config.DEBUG,
        docs_url=config.DOCS_URL,
        openapi_url=config.OPENAPI_URL,
        redoc_url=config.REDOC_URL,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(root_router)
    app.include_router(ws_root_router)

    return app
