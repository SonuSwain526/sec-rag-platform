"""
Generation Service Exceptions for sec-rag.
"""


class GenerationError(Exception):
    """
    Raised when LLM API completion fails.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
