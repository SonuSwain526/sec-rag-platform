"""
Evaluation Service Exceptions for sec-rag.
"""


class EvaluationError(Exception):
    """
    Raised when evaluation logging or calculation fails.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
