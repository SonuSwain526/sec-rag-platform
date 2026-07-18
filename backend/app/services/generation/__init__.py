"""
Generation Service package for sec-rag.

Handles synthesis of contextual documents into user-friendly answers.
"""

from app.services.generation.interfaces import BaseGenerationService
from app.services.generation.service import GenerationService
from app.services.generation.exceptions import GenerationError

__all__ = ["BaseGenerationService", "GenerationService", "GenerationError"]
