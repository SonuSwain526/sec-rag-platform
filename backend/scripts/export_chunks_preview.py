"""
Dumps all chunks from one filing to a readable text file, so we can
actually inspect what a chunk looks like — not yet real storage,
just a visibility tool.
"""
import json
from pathlib import Path
from dataclasses import asdict

from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner
from app.services.metadata.section_tagger import SectionTagger
from app.services.chunking.chunker import Chunker

print("Starting up...")
parser = DoclingParsingService()
cleaner = TableCleaner()
tagger = SectionTagger()
chunker = Chunker()

file_path = Path("data/raw_filings/aapl_2025-10-31.htm")
print(f"Parsing {file_path.name}...")

result = parser.parse(file_path)
doc = result.document
doc = cleaner.clean(doc)

sections = tagger.find_sections(doc)
content_by_section = tagger.get_section_content(doc, sections)
chunks = chunker.chunk_all_sections(content_by_section, sections, company="AAPL", fiscal_year=2025)

output_path = Path("data/processed/aapl_2025_chunks_preview.json")
output_path.write_text(
    json.dumps([asdict(c) for c in chunks], indent=2),
    encoding="utf-8",
)

print(f"Saved {len(chunks)} chunks to: {output_path}")
print("Open that file to browse every chunk with its full content and metadata.")