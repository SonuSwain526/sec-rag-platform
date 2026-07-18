"""
Chunking Service package for sec-rag.

Handles breaking down raw filing texts into manageable semantic contexts.
"""

from app.services.chunking.interfaces import BaseChunkingService
from app.services.chunking.service import ChunkingService
from app.services.chunking.exceptions import ChunkingError

__all__ = ["BaseChunkingService", "ChunkingService", "ChunkingError"]
