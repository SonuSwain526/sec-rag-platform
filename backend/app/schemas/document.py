"""
Document Schemas for sec-rag.

Defines Pydantic models for verifying uploaded SEC filings and detailing processing results.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    """
    Shared attributes for SEC filings.
    """
    filename: str
    ticker: Optional[str] = None
    form_type: Optional[str] = None
    filing_date: Optional[date] = None


class DocumentCreate(DocumentBase):
    """
    Schema for creating or registering a new SEC Document.
    """
    file_path: str


class DocumentChunkResponse(BaseModel):
    """
    Schema for representing document text segment outputs.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    chunk_index: int
    content: str
    vector_id: Optional[str] = None


class DocumentResponse(DocumentBase):
    """
    Full details returned for a processed SEC Document.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_path: str
    status: str
    chunks: List[DocumentChunkResponse] = []
