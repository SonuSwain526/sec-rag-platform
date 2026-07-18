"""
Validation Service Exceptions for sec-rag.
"""


class ValidationError(Exception):
    """
    Raised when validation system fails to execute assertions or checks.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
