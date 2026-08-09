from pathlib import Path

from app.services.parsing.service import DoclingParsingService

parser = DoclingParsingService()

file_path = Path("data/raw_filings/amzn_2024-02-02.htm")
print(f"Parsing {file_path.name}...")

result = parser.parse(file_path)
doc = result.document

print("\n--- Every table containing an 'Item X' cell (one sample row per table) ---\n")

for table_idx, table in enumerate(doc.tables):
    found_row = None
    for row in table.data.grid:
        row_texts = [cell.text.strip() if cell.text else "" for cell in row]
        if any(text.lower().startswith("item ") for text in row_texts):
            found_row = [t for t in row_texts if t]
            break
    if found_row:
        print(f"Table #{table_idx}: {found_row}")