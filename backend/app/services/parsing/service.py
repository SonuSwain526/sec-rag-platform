from pathlib import Path

from docling.document_converter import DocumentConverter
from docling.datamodel.document import ConversionResult

from app.services.parsing.interfaces import DocumentParser
from app.services.parsing.exceptions import ParsingError, UnsupportedFileTypeError

SUPPORTED_EXTENSIONS = {".htm", ".html", ".pdf"}


class DoclingParsingService(DocumentParser):
    """
    Docling-based implementation of DocumentParser.
    Parses SEC 10-K filings (HTML or PDF) into a structured document
    model, preserving heading hierarchy and table structure.
    """

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path: Path) -> ConversionResult:
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {file_path.suffix} (file: {file_path.name})"
            )

        if not file_path.exists():
            raise ParsingError(f"File not found: {file_path}")

        try:
            return self.converter.convert(str(file_path))
        except Exception as e:
            raise ParsingError(f"Docling failed to parse {file_path.name}: {e}") from e