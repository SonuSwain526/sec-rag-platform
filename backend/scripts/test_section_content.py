from pathlib import Path

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner
from app.services.metadata.section_tagger import SectionTagger

print("Starting up...")
parser = DoclingParsingService()
cleaner = TableCleaner()
tagger = SectionTagger()

file_path = Path("data/raw_filings/aapl_2025-10-31.htm")
print(f"Parsing {file_path.name}...")

result = parser.parse(file_path)
doc = result.document
doc = cleaner.clean(doc)

sections = tagger.find_sections(doc)
content_by_section = tagger.get_section_content(doc, sections)

print(f"\n--- Item count per section ---\n")
for section in sections:
    item_count = len(content_by_section[section.item_code])
    print(f"  Item {section.item_code} ({section.title[:50]}): {item_count} items")

# Sanity check: total items across all sections should roughly match
# the document's total item count minus the cover page/TOC items we dropped
total_tagged = sum(len(v) for v in content_by_section.values())
print(f"\nTotal items tagged to a section: {total_tagged}")