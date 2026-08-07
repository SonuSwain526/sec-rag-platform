"""
Runs the complete pipeline on one filing — parse, clean, tag, chunk —
and actually saves the results to the database this time, not just
printing them. Creates a Document row plus its DocumentChunk rows.
"""
from pathlib import Path

from app.db.session import SessionLocal
from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner
from app.services.metadata.section_tagger import SectionTagger
from app.services.chunking.chunker import Chunker
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository

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

print(f"Generated {len(chunks)} chunks. Saving to database...")

db = SessionLocal()
document_repo = DocumentRepository(db)
chunk_repo = ChunkRepository(db)

document = document_repo.create(
    company="AAPL",
    fiscal_year=2025,
    filename=file_path.name,
    file_path=str(file_path),
)
document_repo.update_status(document.id, "chunked")

saved_chunks = chunk_repo.save_chunks(document.id, chunks)

print(f"\nSaved Document id={document.id} with {len(saved_chunks)} chunks.")
print(f"Verify: chunk_repo.count_by_document({document.id}) = {chunk_repo.count_by_document(document.id)}")

db.close()