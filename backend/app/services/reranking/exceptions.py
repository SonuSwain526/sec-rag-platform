"""
Reranking Service Exceptions for sec-rag.
"""


class RerankingError(Exception):
    """
    Raised when cross-encoder execution or API connectivity fails.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
