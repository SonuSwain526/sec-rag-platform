from pathlib import Path

from docling.document_converter import DocumentConverter
from docling.datamodel.document import ConversionResult


class DoclingParser:
    """
    Wraps Docling's DocumentConverter to parse SEC 10-K HTML filings
    into a structured document representation — preserving heading
    hierarchy and table structure, which raw text extraction would lose.
    """

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path: Path) -> ConversionResult:
        """
        Parses a single filing (HTML or PDF) into Docling's structured
        document model. Returns the full conversion result, which includes
        the parsed document plus any parsing metadata/errors.
        """
        result = self.converter.convert(str(file_path))
        return result