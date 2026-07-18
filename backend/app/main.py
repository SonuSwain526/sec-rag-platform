"""
FastAPI Main Entrypoint for sec-rag.

Initializes the FastAPI application instance, sets up middleware configurations,
attaches custom API routers, and defines lifespan startup/shutdown events.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_app_logging, get_logger
from app.api.v1.router import api_router
from app.db.session import engine

# Configure logs
setup_app_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handles application startup and shutdown events.
    """
    logger.info("Initializing sec-rag services...")
    # TODO: Verify database and Qdrant connectivity here
    yield
    logger.info("Shutting down engine resources...")
    # Dispose of connection pools
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Apply CORS origins middleware configurations
# TODO: Fine-tune headers and credentials for production clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root() -> dict:
    """
    Application index info endpoint.
    """
    return {
        "project": settings.PROJECT_NAME,
        "status": "healthy",
        "api_docs_url": "/docs"
    }
