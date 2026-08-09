from pathlib import Path

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner

parser = DoclingParsingService()
cleaner = TableCleaner()

file_path = Path("data/raw_filings/amzn_2024-02-02.htm")
print(f"Parsing {file_path.name}...")

result = parser.parse(file_path)
doc = result.document

print(f"Tables BEFORE cleaning: {len(doc.tables)}")

# Find and print one known heading table (Item 1 / Business) BEFORE cleaning
print("\n--- Table content mentioning 'Business' or 'Item 1' — BEFORE cleaning ---")
for table_idx, table in enumerate(doc.tables):
    for row in table.data.grid:
        row_texts = [cell.text.strip() if cell.text else "" for cell in row]
        non_blank = [t for t in row_texts if t]
        if any("item 1." in t.lower() for t in non_blank) or any("business" == t.lower() for t in non_blank):
            print(f"  Table #{table_idx}: {non_blank}")

# Now clean, and check the SAME thing again
doc = cleaner.clean(doc)
print(f"\nTables AFTER cleaning: {len(doc.tables)}")

print("\n--- Table content mentioning 'Business' or 'Item 1' — AFTER cleaning ---")
for table_idx, table in enumerate(doc.tables):
    for row in table.data.grid:
        row_texts = [cell.text.strip() if cell.text else "" for cell in row]
        non_blank = [t for t in row_texts if t]
        if any("item 1." in t.lower() for t in non_blank) or any("business" == t.lower() for t in non_blank):
            print(f"  Table #{table_idx}: {non_blank}")