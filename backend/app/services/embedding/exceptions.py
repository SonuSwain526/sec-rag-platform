"""
Embedding Service Exceptions for sec-rag.
"""


class EmbeddingError(Exception):
    """
    Raised when vector generation or embedding API connectivity fails.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
