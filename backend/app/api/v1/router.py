"""
API Router configuration for sec-rag.

Registers and namespaces endpoints under the '/api/v1' route prefix.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, documents, query

api_router = APIRouter()

# Include endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
