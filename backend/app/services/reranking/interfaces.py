"""
Reranking Service Interfaces for sec-rag.

Defines protocols to sort and filter raw search outputs.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseRerankingService(ABC):
    """
    Interface for computing cross-attention weights and sorting retrieved documents.
    """
    @abstractmethod
    async def rerank(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Re-scores and reorders retrieval results against the user query.
        
        Args:
            query: User search string.
            results: List of retrieved chunk dictionary maps.
            top_n: Limit of results to return.
            
        Returns:
            Sorted results with updated scores.
        """
        pass
