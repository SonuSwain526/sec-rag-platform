"""
Runs the full pipeline (parse -> clean -> tag -> chunk -> embed -> store)
across every filing in data/raw_filings/. Safe to re-run — already-
processed filings are skipped, so a failure partway through doesn't
lose earlier progress.
"""
import re
from pathlib import Path

from app.db.session import SessionLocal
from app.services.parsing.service import DoclingParsingService
from app.services.cleaning.table_cleaner import TableCleaner
from app.services.metadata.section_tagger import SectionTagger
from app.services.chunking.chunker import Chunker
from app.services.embedding.embedder import Embedder
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.vector_repository import VectorRepository

RAW_FILINGS_DIR = Path("data/raw_filings")
FILENAME_PATTERN = re.compile(r"^([a-z]+)_(\d{4})-\d{2}-\d{2}\.htm$")


def parse_filename(filename: str) -> tuple[str, int]:
    """Extracts (company_ticker, fiscal_year) from a filename like 'aapl_2025-10-31.htm'.
    Fiscal year is approximated from the filing date's year — a reasonable
    simplification for this project's scope, not a precise fiscal-calendar lookup."""
    match = FILENAME_PATTERN.match(filename)
    if not match:
        raise ValueError(f"Filename doesn't match expected pattern: {filename}")
    ticker, year = match.groups()
    return ticker.upper(), int(year)


def process_filing(file_path: Path, db, parser, cleaner, tagger, chunker, embedder, vector_repo) -> None:
    document_repo = DocumentRepository(db)
    chunk_repo = ChunkRepository(db)

    company, fiscal_year = parse_filename(file_path.name)

    # Skip if this exact file was already fully processed
    existing = [d for d in document_repo.list_by_company(company) if d.filename == file_path.name]
    if existing and existing[0].status == "ready":
        print(f"  Skipping (already processed): {file_path.name}")
        return

    print(f"  Parsing {file_path.name} ({company}, FY{fiscal_year})...")
    result = parser.parse(file_path)
    doc = result.document
    doc = cleaner.clean(doc)

    sections = tagger.find_sections(doc)
    content_by_section = tagger.get_section_content(doc, sections)
    
    chunks = chunker.chunk_all_sections(content_by_section, sections, company=company, fiscal_year=fiscal_year)
    print(f"    Generated {len(chunks)} chunks.")

    if not chunks:
        raise ValueError(
            f"No sections/chunks detected for {file_path.name} — "
            f"SectionTagger likely doesn't match this filer's heading format."
        )

    document = document_repo.create(
        company=company, fiscal_year=fiscal_year, filename=file_path.name, file_path=str(file_path)
    )
    saved_chunks = chunk_repo.save_chunks(document.id, chunks)

    print(f"    Embedding {len(saved_chunks)} chunks...")
    texts = [c.content for c in saved_chunks]
    vectors = embedder.embed_batch(texts)

    payloads = [
        {
            "company": c.company,
            "fiscal_year": c.fiscal_year,
            "item_code": c.item_code,
            "item_title": c.item_title,
            "chunk_type": c.chunk_type,
            "content": c.content,
            "sqlite_chunk_id": c.id,
        }
        for c in saved_chunks
    ]
    point_ids = vector_repo.upsert_chunks(
        chunk_ids=[c.id for c in saved_chunks], vectors=vectors, payloads=payloads
    )

    for chunk, point_id in zip(saved_chunks, point_ids):
        chunk.vector_id = point_id
    db.commit()

    document_repo.update_status(document.id, "ready")
    print(f"    Done: Document id={document.id}, {len(saved_chunks)} chunks stored.")




def main() -> None:
    print("Loading models (this happens once, then reused for all filings)...")
    parser = DoclingParsingService()
    cleaner = TableCleaner()
    tagger = SectionTagger()
    chunker = Chunker()
    embedder = Embedder()

    vector_repo = VectorRepository()
    vector_repo.ensure_collection()

    db = SessionLocal()

    html_files = sorted(RAW_FILINGS_DIR.glob("*.htm"))
    print(f"\nFound {len(html_files)} filings to process.\n")

    succeeded, failed = 0, []
    for file_path in html_files:
        print(f"[{succeeded + len(failed) + 1}/{len(html_files)}] {file_path.name}")
        try:
            process_filing(file_path, db, parser, cleaner, tagger, chunker, embedder, vector_repo)
            succeeded += 1
        except Exception as e:
            print(f"    FAILED: {e}")
            failed.append((file_path.name, str(e)))
        print()

    db.close()

    print("=" * 60)
    print(f"Done. {succeeded}/{len(html_files)} filings processed successfully.")
    if failed:
        print(f"\n{len(failed)} failures:")
        for name, error in failed:
            print(f"  - {name}: {error}")


if __name__ == "__main__":
    main()