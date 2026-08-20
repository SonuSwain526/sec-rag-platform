"""
Rebuilds the Qdrant Cloud collection directly from SQLite chunks —
re-embeds existing chunk text (no re-parsing needed) and uploads
fresh. Used to recover from a Qdrant collection dimension mismatch
without repeating the full multi-hour parsing pipeline.
"""
import time

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, PayloadSchemaType

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder

settings = get_settings()

print("Loading all chunks from SQLite...")
db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()
print(f"Loaded {len(all_chunks)} chunks.")

print("Loading embedding model...")
embedder = Embedder()

print(f"Embedding all {len(all_chunks)} chunks (this will take a while)...")
texts = [c.content for c in all_chunks]
vectors = embedder.embed_batch(texts)
print(f"Done embedding. Vector dimension: {len(vectors[0])}")

client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY, timeout=60)

print(f"Recreating collection '{settings.QDRANT_COLLECTION_NAME}' with correct dimension...")
existing = [c.name for c in client.get_collections().collections]
if settings.QDRANT_COLLECTION_NAME in existing:
    client.delete_collection(settings.QDRANT_COLLECTION_NAME)
    print("  Deleted old collection.")

client.create_collection(
    collection_name=settings.QDRANT_COLLECTION_NAME,
    vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
)
client.create_payload_index(
    collection_name=settings.QDRANT_COLLECTION_NAME,
    field_name="company",
    field_schema=PayloadSchemaType.KEYWORD,
)
print("  Created fresh collection with payload index.")

print("Uploading in batches...")
BATCH_SIZE = 50
MAX_RETRIES = 3

import uuid

for i in range(0, len(all_chunks), BATCH_SIZE):
    batch_chunks = all_chunks[i:i + BATCH_SIZE]
    batch_vectors = vectors[i:i + BATCH_SIZE]

    points = []
    for chunk, vector in zip(batch_chunks, batch_vectors):
        point_id = str(uuid.uuid4())
        points.append(PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "company": chunk.company,
                "fiscal_year": chunk.fiscal_year,
                "item_code": chunk.item_code,
                "item_title": chunk.item_title,
                "chunk_type": chunk.chunk_type,
                "content": chunk.content,
                "sqlite_chunk_id": chunk.id,
            },
        ))
        chunk.vector_id = point_id

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client.upsert(collection_name=settings.QDRANT_COLLECTION_NAME, points=points)
            print(f"  Uploaded {min(i + BATCH_SIZE, len(all_chunks))}/{len(all_chunks)}...")
            break
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise
            time.sleep(attempt * 3)

db.commit()
db.close()

print("Verifying...")
count = client.count(settings.QDRANT_COLLECTION_NAME).count
print(f"Cloud collection now has {count} points with dimension {len(vectors[0])}.")