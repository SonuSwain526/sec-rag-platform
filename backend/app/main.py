from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once at startup, then once at shutdown.
    This is where we'll later load embedding/reranker models into
    memory (Phase 8+) so they aren't reloaded on every request.
    """
    setup_logging()
    # Startup logic goes here (e.g., warm up ML models, check Qdrant connection)
    yield
    # Shutdown logic goes here (e.g., close DB connections gracefully)


def create_app() -> FastAPI:
    """
    Application factory. Builds and returns a configured FastAPI instance.
    Keeping this in a function (not module-level `app = FastAPI()`)
    makes the app testable — tests can call create_app() to get a
    fresh instance without import-time side effects.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()