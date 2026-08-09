from pathlib import Path

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner
from app.services.metadata.section_tagger import SectionTagger

parser = DoclingParsingService()
cleaner = TableCleaner()
tagger = SectionTagger()

for filename in ["aapl_2025-10-31.htm", "amzn_2024-02-02.htm"]:
    file_path = Path("data/raw_filings") / filename
    print(f"\n=== {filename} ===")

    result = parser.parse(file_path)
    doc = result.document
    doc = cleaner.clean(doc)

    sections = tagger.find_sections(doc)
    print(f"Found {len(sections)} sections:")
    for s in sections:
        print(f"  Item {s.item_code}: {s.title}")