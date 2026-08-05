"""
Diagnostic: checks what label types Docling actually assigned to text
in this document, and searches for "Item X." patterns regardless of
label, to see how SEC's section headers are actually represented.
"""
from collections import Counter
from pathlib import Path

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner

print("Starting up — loading Docling parser...")

parser = DoclingParsingService()
cleaner = TableCleaner()

file_path = Path("data/raw_filings/aapl_2025-10-31.htm")
print(f"Parsing {file_path.name} — this can take 1-3 minutes...")

result = parser.parse(file_path)
doc = result.document
doc = cleaner.clean(doc)

# Count how many text items exist per label type
label_counts = Counter(str(text_item.label) for text_item in doc.texts)
print("\n--- Label types found in doc.texts ---")
for label, count in label_counts.most_common():
    print(f"  {label}: {count}")

# Search for "Item X." pattern regardless of label
print("\n--- Text items matching 'Item <number>' pattern (first 20) ---")
match_count = 0
for text_item in doc.texts:
    text = text_item.text.strip() if text_item.text else ""
    if text.startswith("Item ") and len(text) < 100:
        print(f"  [label={text_item.label}] {text}")
        match_count += 1
        if match_count >= 20:
            break

print(f"\nTotal 'Item ...' matches shown: {match_count}")