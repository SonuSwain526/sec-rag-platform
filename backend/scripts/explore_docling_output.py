"""
Exploratory script — parses one filing and inspects Docling's output
structure, so we understand the data shape before writing real chunking
logic against it.
"""
from pathlib import Path

from app.services.parsing.docling_parser import DoclingParser

parser = DoclingParser()

file_path = Path("data/raw_filings/aapl_2025-10-31.htm")
print(f"Parsing: {file_path} ({file_path.stat().st_size / 1024:.0f} KB)")

result = parser.parse(file_path)
doc = result.document

markdown_output = doc.export_to_markdown()

output_path = Path("data/processed/aapl_2025-10-31_preview.md")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(markdown_output, encoding="utf-8")

print(f"Exported markdown preview to: {output_path}")
print(f"Markdown length: {len(markdown_output)} characters")

print("\n--- Preview (first 2000 chars) ---")
print(markdown_output[:2000])