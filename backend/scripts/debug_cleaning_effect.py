from pathlib import Path

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner

parser = DoclingParsingService()
cleaner = TableCleaner()

file_path = Path("data/raw_filings/amzn_2024-02-02.htm")
print(f"Parsing {file_path.name}...")

result = parser.parse(file_path)
doc = result.document

print(f"Tables before cleaning: {len(doc.tables)}")

# Run the REAL clean() method, step by step, printing what happens
empty_tables = [t for t in doc.tables if cleaner._is_empty_table(t)]
print(f"Tables flagged as empty (about to be deleted): {len(empty_tables)}")

# Check: are our two target tables in the deletion list?
target_refs = set()
for table in doc.tables:
    for row in table.data.grid:
        row_texts = [c.text.strip() if c.text else "" for c in row]
        if any("item 1." in t.lower() for t in row_texts):
            target_refs.add(table.self_ref)

print(f"Target table refs (Item 1 heading tables): {target_refs}")
empty_refs = {t.self_ref for t in empty_tables}
print(f"Overlap between target tables and tables-flagged-empty: {target_refs & empty_refs}")

if empty_tables:
    doc.delete_items(node_items=empty_tables)

print(f"\nTables immediately after delete_items(): {len(doc.tables)}")

# Now check: do our target tables still exist in doc.tables at all?
remaining_refs = {t.self_ref for t in doc.tables}
print(f"Target refs still present after delete_items(): {target_refs & remaining_refs}")
print(f"Target refs MISSING after delete_items(): {target_refs - remaining_refs}")