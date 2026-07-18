"""
Evaluation Service package for sec-rag.

Handles system-wide performance scoring, trace metrics, and user feedback metrics.
"""

from app.services.evaluation.interfaces import BaseEvaluationService
from app.services.evaluation.service import EvaluationService
from app.services.evaluation.exceptions import EvaluationError

__all__ = ["BaseEvaluationService", "EvaluationService", "EvaluationError"]
