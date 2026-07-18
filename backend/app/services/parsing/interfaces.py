"""
Parsing Service Interfaces for sec-rag.

Defines the core interface protocol for raw document text extractors.
"""

from abc import ABC, abstractmethod


class BaseParsingService(ABC):
    """
    Interface for parsing raw SEC filings into uniform plain text formats.
    """
    @abstractmethod
    async def parse_file(self, file_path: str) -> str:
        """
        Parses a file and extracts its text contents.
        
        Args:
            file_path: The absolute path of the file to process.
            
        Returns:
            The extracted text content as a string.
            
        Raises:
            ParsingError: If extraction fails or format is unsupported.
        """
        pass
