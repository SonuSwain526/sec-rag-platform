"""
Query Schemas for sec-rag.

Defines Pydantic models for incoming RAG search queries and generated text responses.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    Validation schema for processing user search requests.
    """
    query: str = Field(..., min_length=3, description="The query string to run search retrieval and response generation on.")
    ticker: Optional[str] = Field(None, description="Optional corporate ticker symbol to restrict document context (e.g. AAPL).")
    form_type: Optional[str] = Field(None, description="Optional SEC filing form type (e.g., 10-K, 10-Q).")
    top_k: int = Field(default=5, ge=1, le=20, description="The number of source chunks to retrieve for LLM input.")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Additional custom metadata filtering parameters.")


class SourceChunk(BaseModel):
    """
    Schema representing a reference text segment retrieved as source context.
    """
    document_id: int
    filename: str
    chunk_index: int
    content: str
    score: float = Field(..., description="Similarity score of the retrieved chunk.")


class QueryResponse(BaseModel):
    """
    Response schema returning generated text answer along with source document citations.
    """
    query: str
    answer: str
    sources: List[SourceChunk] = Field(default_factory=list, description="Reference citations used to generate the answer.")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Processing stats, tokens consumed, or duration details.")
