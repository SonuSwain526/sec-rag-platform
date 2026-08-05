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

print(f"\nFound {len(sections)} real sections:\n")
for section in sections:
    print(f"  Item {section.item_code}: {section.title}")