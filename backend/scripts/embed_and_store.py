from app.db.session import SessionLocal
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.vector_repository import VectorRepository
from app.services.embedding.embedder import Embedder

DOCUMENT_ID = 2

print("Loading chunks from database...")
db = SessionLocal()
chunk_repo = ChunkRepository(db)
chunks = chunk_repo.get_by_document(DOCUMENT_ID)
print(f"Loaded {len(chunks)} chunks.")

print("Loading embedding model...")
embedder = Embedder()

print("Embedding all chunks (this may take a couple minutes on CPU)...")
texts = [c.content for c in chunks]
vectors = embedder.embed_batch(texts)

print("Connecting to Qdrant...")
vector_repo = VectorRepository()
vector_repo.ensure_collection()

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
    for c in chunks
]

print("Storing vectors in Qdrant...")
point_ids = vector_repo.upsert_chunks(
    chunk_ids=[c.id for c in chunks], vectors=vectors, payloads=payloads
)

print("Linking vector IDs back to SQLite...")
for chunk, point_id in zip(chunks, point_ids):
    chunk.vector_id = point_id
db.commit()

print(f"\nDone. {len(chunks)} chunks embedded and stored in Qdrant, linked back to SQLite.")