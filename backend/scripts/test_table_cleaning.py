from pathlib import Path

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner

print("Starting up — loading Docling parser...")  # NEW — confirms the script is actually running

parser = DoclingParsingService()
cleaner = TableCleaner()

file_path = Path("data/raw_filings/aapl_2025-10-31.htm")
print(f"Parsing {file_path.name} — this can take 1-3 minutes for a large filing...")  # NEW

result = parser.parse(file_path)
doc = result.document

print(f"Tables before cleaning: {len(doc.tables)}")

empty_check_count = len(doc.tables)
doc = cleaner.clean(doc)

print(f"Tables after cleaning: {len(doc.tables)}")

markdown_output = doc.export_to_markdown()
output_path = Path("data/processed/aapl_2025-10-31_cleaned.md")
output_path.write_text(markdown_output, encoding="utf-8")

print(f"Cleaned markdown saved to: {output_path}")
print(f"Cleaned markdown length: {len(markdown_output)} characters")

print("\n--- Cleaned preview (first 2000 chars) ---")
print(markdown_output[:2000])