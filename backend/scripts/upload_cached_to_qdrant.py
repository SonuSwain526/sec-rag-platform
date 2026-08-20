"""
Uploads previously-cached embeddings (from embed_and_cache.py) to
Qdrant Cloud. Safe to re-run if it fails partway — doesn't touch
the embedding step at all.
"""
import pickle
import time
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, PayloadSchemaType

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk

settings = get_settings()

print("Loading cached embeddings...")
with open("embedding_cache.pkl", "rb") as f:
    cache = pickle.load(f)

vectors = cache["vectors"]
chunk_ids = cache["chunk_ids"]
payloads = cache["payloads"]
print(f"Loaded {len(vectors)} cached vectors (dim={len(vectors[0])}).")

client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY, timeout=120)

existing = [c.name for c in client.get_collections().collections]
current_count = 0
if settings.QDRANT_COLLECTION_NAME in existing:
    current_count = client.count(settings.QDRANT_COLLECTION_NAME).count

if settings.QDRANT_COLLECTION_NAME not in existing:
    print("Creating fresh collection...")
    client.create_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
    )
    client.create_payload_index(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        field_name="company",
        field_schema=PayloadSchemaType.KEYWORD,
    )
elif current_count > 0:
    print(f"Collection already has {current_count} points — clearing before re-upload to avoid duplicates...")
    client.delete_collection(settings.QDRANT_COLLECTION_NAME)
    client.create_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
    )
    client.create_payload_index(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        field_name="company",
        field_schema=PayloadSchemaType.KEYWORD,
    )

BATCH_SIZE = 25  # smaller than before, to be extra conservative
MAX_RETRIES = 5

db = SessionLocal()

for i in range(0, len(vectors), BATCH_SIZE):
    batch_vectors = vectors[i:i + BATCH_SIZE]
    batch_ids = chunk_ids[i:i + BATCH_SIZE]
    batch_payloads = payloads[i:i + BATCH_SIZE]

    points = []
    for vector, chunk_id, payload in zip(batch_vectors, batch_ids, batch_payloads):
        point_id = str(uuid.uuid4())
        points.append(PointStruct(id=point_id, vector=vector, payload=payload))

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client.upsert(collection_name=settings.QDRANT_COLLECTION_NAME, points=points)
            print(f"  Uploaded {min(i + BATCH_SIZE, len(vectors))}/{len(vectors)}...")
            break
        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"  FAILED batch at {i} after {MAX_RETRIES} attempts: {e}")
                raise
            wait = attempt * 5
            print(f"  Batch at {i} failed (attempt {attempt}/{MAX_RETRIES}), retrying in {wait}s...")
            time.sleep(wait)

db.close()

print("Verifying...")
count = client.count(settings.QDRANT_COLLECTION_NAME).count
print(f"Cloud collection now has {count} points.")