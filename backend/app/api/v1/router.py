from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, query

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(query.router, tags=["query"])