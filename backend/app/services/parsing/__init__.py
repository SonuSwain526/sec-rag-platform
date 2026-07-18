"""
Parsing Service package for sec-rag.

Handles converting raw SEC documents (HTML/PDF/XBRL) to clean plaintext structures.
"""

from app.services.parsing.interfaces import BaseParsingService
from app.services.parsing.service import ParsingService
from app.services.parsing.exceptions import ParsingError

__all__ = ["BaseParsingService", "ParsingService", "ParsingError"]
