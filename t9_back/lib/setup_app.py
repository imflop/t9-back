import typing as t

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import Middleware

from t9_back import __module_name__, __version__

from ..api.v1.health import router as health
from ..api.v1.shorter import router as shorter
from ..api.v1.users import router as users
from ..api.v1.version import router as version
from .settings import SETTINGS_KEY, AppSettings


API_PREFIX = "/api/v1"


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(health, prefix=f"{API_PREFIX}/check", tags=["health"])
    app.include_router(version, prefix=f"{API_PREFIX}/check", tags=["version"])
    app.include_router(shorter, prefix=f"{API_PREFIX}", tags=["shorter"])
    app.include_router(users, prefix=f"{API_PREFIX}/users", tags=["users"])
    return app


def add_origins() -> t.Sequence[str]:
    return "http://localhost:3000", "http://0.0.0.0:3000", "http://api:3000"


def setup_app(settings: AppSettings) -> FastAPI:
    settings.configure_logging()

    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_hosts or add_origins(),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    if settings.sentry_dsn:
        sentry_sdk.init(dsn=settings.sentry_dsn, release=__version__)
        middlewares.append(Middleware(SentryAsgiMiddleware))

    app = FastAPI(
        title=__module_name__,
        version=__version__,
        description="t9 back",
        middleware=middlewares,
        default_response_class=ORJSONResponse,
        **{SETTINGS_KEY: settings},  # type: ignore
    )

    app = register_routers(app)

    return app
