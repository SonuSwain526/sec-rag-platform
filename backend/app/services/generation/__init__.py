"""
Generation package for sec-rag.

Exposes the Groq LLM client, prompt builder, and the full RAG
orchestration service that ties retrieval + generation together.
"""
from app.services.generation.groq_client import GroqClient
from app.services.generation.prompt_builder import PromptBuilder, SYSTEM_PROMPT
from app.services.generation.rag_service import RagService

__all__ = ["GroqClient", "PromptBuilder", "SYSTEM_PROMPT", "RagService"]