"""
Loads chunks we already saved to the database (from the previous step)
and embeds them, to confirm the embedding model works and inspect
vector output before wiring it into the real pipeline.
"""
from app.db.session import SessionLocal
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding.embedder import Embedder

print("Loading chunks from database...")
db = SessionLocal()
chunk_repo = ChunkRepository(db)

DOCUMENT_ID = 2  # the AAPL document we saved in the last step
chunks = chunk_repo.get_by_document(DOCUMENT_ID)
print(f"Loaded {len(chunks)} chunks for document_id={DOCUMENT_ID}")

print("\nLoading embedding model (BAAI/bge-large-en-v1.5) — first run downloads the model, may take a few minutes...")
embedder = Embedder()

# Just embed the first 5 chunks for a quick sanity check before doing all 180
sample_chunks = chunks[:5]
sample_texts = [c.content for c in sample_chunks]

print(f"\nEmbedding {len(sample_texts)} sample chunks...")
vectors = embedder.embed_batch(sample_texts)

print(f"\nGenerated {len(vectors)} vectors.")
print(f"Vector dimension: {len(vectors[0])}")
print(f"First 5 values of vector 1: {vectors[0][:10]}")

db.close()