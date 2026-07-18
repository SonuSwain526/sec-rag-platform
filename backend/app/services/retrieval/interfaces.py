"""
Retrieval Service Interfaces for sec-rag.

Defines protocols to fetch relevant document context from the search systems.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRetrievalService(ABC):
    """
    Interface for query processing and document context retrieval.
    """
    @abstractmethod
    async def retrieve_context(
        self,
        query: str,
        ticker: Optional[str] = None,
        form_type: Optional[str] = None,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves matching document chunks based on a raw user query.
        
        Args:
            query: The user text search string.
            ticker: Corporate ticker to limit scope.
            form_type: Form type to restrict context.
            top_k: Number of chunks to return.
            filters: Custom dictionary rules.
            
        Returns:
            List of dictionary payloads detailing text fragments and scores.
        """
        pass
