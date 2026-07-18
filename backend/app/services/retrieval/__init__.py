"""
Retrieval Service package for sec-rag.

Handles query embedding formulation and vector store match searches.
"""

from app.services.retrieval.interfaces import BaseRetrievalService
from app.services.retrieval.service import RetrievalService
from app.services.retrieval.exceptions import RetrievalError

__all__ = ["BaseRetrievalService", "RetrievalService", "RetrievalError"]
