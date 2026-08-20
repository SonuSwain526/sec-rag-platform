"""
Embeds all SQLite chunks and saves the vectors + metadata to a local
file. Separating this from the upload step means a failed/timed-out
upload can be retried without redoing the expensive embedding work.
"""
import json
import pickle

from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder

print("Loading chunks from SQLite...")
db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()
print(f"Loaded {len(all_chunks)} chunks.")

print("Loading embedding model...")
embedder = Embedder()

print(f"Embedding {len(all_chunks)} chunks (this takes a while)...")
texts = [c.content for c in all_chunks]
vectors = embedder.embed_batch(texts)
print(f"Done. Vector dimension: {len(vectors[0])}")

cache_data = {
    "vectors": vectors,
    "chunk_ids": [c.id for c in all_chunks],
    "payloads": [
        {
            "company": c.company,
            "fiscal_year": c.fiscal_year,
            "item_code": c.item_code,
            "item_title": c.item_title,
            "chunk_type": c.chunk_type,
            "content": c.content,
            "sqlite_chunk_id": c.id,
        }
        for c in all_chunks
    ],
}

with open("embedding_cache.pkl", "wb") as f:
    pickle.dump(cache_data, f)

print(f"Saved embeddings to embedding_cache.pkl ({len(vectors)} vectors, dim={len(vectors[0])})")
db.close()