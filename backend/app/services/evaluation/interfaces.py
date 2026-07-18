"""
Evaluation Service Interfaces for sec-rag.

Defines protocols to collect and log telemetry quality scores.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseEvaluationService(ABC):
    """
    Interface for tracking system latency, user-feedback scores, and context recall accuracy.
    """
    @abstractmethod
    async def evaluate_pipeline(
        self,
        query: str,
        answer: str,
        contexts: List[Dict[str, Any]],
        validation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates QA metrics (faithfulness, answer relevance, context recall).
        
        Args:
            query: The search request query.
            answer: The generated answer.
            contexts: List of source contexts.
            validation_results: Output of the validation step.
            
        Returns:
            Dictionary containing metrics logs.
        """
        pass
