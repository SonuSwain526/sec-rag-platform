"""
Parsing package for sec-rag.

Exposes the document parsing interface and its Docling-based implementation.
"""
from app.services.parsing.interfaces import DocumentParser
from app.services.parsing.service import DoclingParsingService

__all__ = ["DocumentParser", "DoclingParsingService"]