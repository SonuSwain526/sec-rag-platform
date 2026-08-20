"""
Removes duplicate Document rows (and their chunks) that accumulated
from repeated pipeline runs failing partway through. Keeps only the
MOST RECENT document per filename, deletes older duplicates and all
their associated chunks.
"""
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.chunk import DocumentChunk

db = SessionLocal()

all_docs = db.query(Document).order_by(Document.filename, Document.id).all()

by_filename: dict[str, list[Document]] = {}
for doc in all_docs:
    by_filename.setdefault(doc.filename, []).append(doc)

total_deleted_docs = 0
total_deleted_chunks = 0

for filename, docs in by_filename.items():
    if len(docs) <= 1:
        continue
    # Keep the LAST (highest id = most recent) document, delete the rest
    docs_to_delete = docs[:-1]
    kept = docs[-1]
    print(f"{filename}: {len(docs)} copies found, keeping id={kept.id} (status={kept.status}), deleting {len(docs_to_delete)} older copies")

    for doc in docs_to_delete:
        chunk_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).count()
        db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()
        db.delete(doc)
        total_deleted_docs += 1
        total_deleted_chunks += chunk_count

db.commit()

remaining_docs = db.query(Document).count()
remaining_chunks = db.query(DocumentChunk).count()

print(f"\nDeleted {total_deleted_docs} duplicate documents, {total_deleted_chunks} orphaned chunks.")
print(f"Remaining: {remaining_docs} documents, {remaining_chunks} chunks.")

db.close()