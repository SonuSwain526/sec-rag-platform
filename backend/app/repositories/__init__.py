"""
Repositories package for sec-rag.

Encapsulates all database access for each model, keeping services
and API endpoints free of raw SQLAlchemy queries.
"""
from app.repositories.document_repository import DocumentRepository

__all__ = ["DocumentRepository"]