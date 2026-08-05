from pathlib import Path

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

chunks = chunker.chunk_all_sections(
    content_by_section, sections, company="AAPL", fiscal_year=2025
)

print(f"\nTotal chunks created: {len(chunks)}")

text_chunks = [c for c in chunks if c.chunk_type == "text"]
table_chunks = [c for c in chunks if c.chunk_type == "table"]
print(f"  Text chunks: {len(text_chunks)}")
print(f"  Table chunks: {len(table_chunks)}")

avg_tokens = sum(c.token_count for c in text_chunks) / len(text_chunks) if text_chunks else 0
print(f"  Average text chunk size: {avg_tokens:.0f} tokens")

print("\n--- Sample: first 3 chunks ---\n")
for chunk in chunks[:3]:
    print(f"[{chunk.chunk_type.upper()} | Item {chunk.item_code} | {chunk.token_count} tokens]")
    print(chunk.content[:300])
    print("---")