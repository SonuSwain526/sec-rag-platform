from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class DocumentParser(ABC):
    """
    Abstract contract for any document parser implementation.
    Services and endpoints should depend on this interface, not on
    a specific parser class — keeps the rest of the app decoupled
    from Docling specifically.
    """

    @abstractmethod
    def parse(self, file_path: Path) -> Any:
        """Parse a document file and return its structured representation."""
        raise NotImplementedError