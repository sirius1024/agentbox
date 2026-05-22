"""FastAPI application factory."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..db.database import init_db
from ..services.errors import ConflictError, NotFoundError, ValidationError
from .routers import agents, health, owners, secrets, settings


@asynccontextmanager
async def _lifespan(app: FastAPI):  # pragma: no cover - trivial
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="AgentBox", version="0.1.0", lifespan=_lifespan)

    @app.exception_handler(NotFoundError)
    async def _not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def _conflict(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def _bad_request(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    app.include_router(health.router)
    app.include_router(owners.router)
    app.include_router(agents.router)
    app.include_router(settings.router)
    app.include_router(secrets.router)
    return app


# Module-level app for ``uvicorn agentbox.api.app:app``.
app = create_app()
