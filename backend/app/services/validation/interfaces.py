"""
Validation Service Interfaces for sec-rag.

Defines protocols for factuality and grounding validation of generated answers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseValidationService(ABC):
    """
    Interface for verifying that generated answers are grounded in provided contexts.
    """
    @abstractmethod
    async def validate_answer(
        self,
        query: str,
        answer: str,
        contexts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Runs validation checks (e.g. self-consistency, contradiction search, grounding).
        
        Args:
            query: The user search query.
            answer: The generated response.
            contexts: List of source contexts utilized.
            
        Returns:
            Dictionary containing compliance status, float score, and issues list.
        """
        pass
