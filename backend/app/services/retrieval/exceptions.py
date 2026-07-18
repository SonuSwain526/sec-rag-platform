"""
Retrieval Service Exceptions for sec-rag.
"""


class RetrievalError(Exception):
    """
    Raised when document context retrieval or search fails.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
