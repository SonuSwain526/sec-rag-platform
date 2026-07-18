"""
Embedding Service package for sec-rag.

Handles generating dense vector representation embeddings for text inputs.
"""

from app.services.embedding.interfaces import BaseEmbeddingService
from app.services.embedding.service import EmbeddingService
from app.services.embedding.exceptions import EmbeddingError

__all__ = ["BaseEmbeddingService", "EmbeddingService", "EmbeddingError"]
