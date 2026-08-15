"""
Copies all points from the local Qdrant collection to a Qdrant Cloud
cluster. Run once, when preparing for deployment — avoids re-running
the expensive embedding pipeline just to move where vectors live.
Safe to re-run: skips collection creation if it already exists, and
upserts are idempotent (same point ID overwrites, not duplicates).
"""
import time

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from app.core.config import get_settings

settings = get_settings()

local_client = QdrantClient(url="http://localhost:6333")

CLOUD_URL = ""
CLOUD_API_KEY = ""

# Longer timeout (in seconds) — the free tier can be slow to respond,
# the default client timeout is too short for that.
cloud_client = QdrantClient(url=CLOUD_URL, api_key=CLOUD_API_KEY, timeout=60)

COLLECTION_NAME = settings.QDRANT_COLLECTION_NAME

print("Fetching collection info from local Qdrant...")
local_info = local_client.get_collection(COLLECTION_NAME)
vector_size = local_info.config.params.vectors.size

existing_collections = [c.name for c in cloud_client.get_collections().collections]
if COLLECTION_NAME not in existing_collections:
    print(f"Creating collection '{COLLECTION_NAME}' on Qdrant Cloud (size={vector_size})...")
    cloud_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
else:
    print(f"Collection '{COLLECTION_NAME}' already exists on Qdrant Cloud — skipping creation.")

print("Fetching all points from local Qdrant...")
all_points = []
offset = None
while True:
    points, offset = local_client.scroll(
        collection_name=COLLECTION_NAME, limit=100, offset=offset, with_vectors=True
    )
    all_points.extend(points)
    if offset is None:
        break

print(f"Found {len(all_points)} points. Uploading to Qdrant Cloud in batches...")

BATCH_SIZE = 50  # smaller batches — more requests, but each one is lighter and less likely to time out
MAX_RETRIES = 3

for i in range(0, len(all_points), BATCH_SIZE):
    batch_points = all_points[i:i + BATCH_SIZE]
    batch = [PointStruct(id=p.id, vector=p.vector, payload=p.payload) for p in batch_points]

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            cloud_client.upsert(collection_name=COLLECTION_NAME, points=batch)
            print(f"  Uploaded {min(i + BATCH_SIZE, len(all_points))}/{len(all_points)} points...")
            break
        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"  FAILED batch starting at {i} after {MAX_RETRIES} attempts: {e}")
                raise
            wait = attempt * 3
            print(f"  Batch starting at {i} failed (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {wait}s...")
            time.sleep(wait)

print("Migration complete. Verifying...")
cloud_count = cloud_client.count(COLLECTION_NAME).count
print(f"Cloud collection now has {cloud_count} points.")