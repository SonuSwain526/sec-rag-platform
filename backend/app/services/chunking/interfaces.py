"""
Chunking Service Interfaces for sec-rag.

Defines protocols for segmentation of large texts into structured chunks.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseChunkingService(ABC):
    """
    Interface for segmenting document text content into semantic chunks.
    """
    @abstractmethod
    async def split_text(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Splits text content into a list of chunks, each retaining metadata.
        
        Args:
            text: The full text string.
            chunk_size: Target size of each chunk (characters or tokens).
            chunk_overlap: Overlapping window size.
            
        Returns:
            List of dictionaries containing chunk_index, content, and chunk_metadata.
        """
        pass
