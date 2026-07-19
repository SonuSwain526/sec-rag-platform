"""
Repositories package for sec-rag.

Encapsulates all database access for each model, keeping services
and API endpoints free of raw SQLAlchemy queries.
"""
from app.repositories.document_repository import DocumentRepository
from app.repositories.user_repository import UserRepository

__all__ = ["DocumentRepository", "UserRepository"]