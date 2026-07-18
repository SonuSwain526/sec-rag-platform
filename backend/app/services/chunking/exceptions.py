"""
Chunking Service Exceptions for sec-rag.
"""


class ChunkingError(Exception):
    """
    Raised when document text segmentation fails.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
