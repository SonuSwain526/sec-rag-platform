"""
Embedding Service Interfaces for sec-rag.

Defines protocols for vector embedding generation.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingService(ABC):
    """
    Interface for translating plaintext blocks into multidimensional vector embeddings.
    """
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single string into a float vector.
        """
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds multiple text strings concurrently.
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Returns the output dimension size of the embedding model.
        """
        pass
