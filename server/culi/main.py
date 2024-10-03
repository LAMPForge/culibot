from typing import TypedDict, AsyncIterator

import structlog
from fastapi import FastAPI
from starlette.types import Scope

from culi.config import settings
from culi.exception_handlers import add_exception_handlers
from culi.common.cors import CORSConfig, CORSMatcherMiddleware
from culi.logging import Logger
from culi.middlewares import PathRewriteMiddleware
from culi.openapi import set_openapi_generator, OPENAPI_PARAMETERS, APITag
from culi.routing import APIRoute
from culi.common.db.postgres import (
    AsyncEngine,
    AsyncSessionMaker,
    Engine,
    SyncSessionMaker,
)
from culi.health.endpoints import router as health_router
from culi.api import router
from culi.logging import configure as configure_logging


log: Logger = structlog.get_logger()


def configure_cors(app: FastAPI) -> None:
    configs: list[CORSConfig] = []

    if settings.CORS_ORIGINS:
        def polar_frontend_matcher(origin: str, scope: Scope) -> bool:
            return origin in settings.CORS_ORIGINS

        polar_frontend_config = CORSConfig(
            polar_frontend_matcher,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        configs.append(polar_frontend_config)

    # External API calls CORS configuration
    api_config = CORSConfig(
        lambda origin, scope: True,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["Authorization"],
    )
    configs.append(api_config)

    app.add_middleware(CORSMatcherMiddleware, configs=configs)


def generate_unique_openapi_id(route: APIRoute) -> str:
    parts = [str(tag) for tag in route.tags if tag not in APITag] + [route.name]
    return ":".join(parts)


class State(TypedDict):
    async_engine: AsyncEngine
    async_sessionmaker: AsyncSessionMaker
    sync_engine: Engine
    sync_sessionmaker: SyncSessionMaker


def create_app() -> FastAPI:
    app = FastAPI(**OPENAPI_PARAMETERS)
    configure_cors(app)

    app.add_middleware(PathRewriteMiddleware, pattern=r"^/api/v1", replacement="/v1")

    add_exception_handlers(app)

    # /health and /ready
    app.include_router(health_router)
    app.include_router(router)

    return app


configure_logging(logfire=True)

app = create_app()
set_openapi_generator(app)