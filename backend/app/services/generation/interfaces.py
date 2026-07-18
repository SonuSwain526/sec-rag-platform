"""
Generation Service Interfaces for sec-rag.

Defines protocols to synthesize responses using LLM endpoints.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseGenerationService(ABC):
    """
    Interface for assembling prompts and requesting text completions from LLMs.
    """
    @abstractmethod
    async def generate_answer(
        self,
        query: str,
        contexts: List[Dict[str, Any]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Assembles a context-rich prompt and calls an LLM to generate the final answer.
        
        Args:
            query: User text search query.
            contexts: List of document chunks containing raw text.
            system_prompt: Optional instruction guidelines.
            
        Returns:
            The synthesized answer string.
        """
        pass
from typing import Optional
