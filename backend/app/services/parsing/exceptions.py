"""
Parsing Service Exceptions for sec-rag.
"""


class ParsingError(Exception):
    """
    Raised when document parsing or extraction fails.
    """
    def __init__(self, message: str, details: str = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details
