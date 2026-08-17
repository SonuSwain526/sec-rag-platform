import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchAny

from app.core.config import get_settings

settings = get_settings()


class VectorRepository:
    """
    Handles all interaction with Qdrant — creating the collection,
    storing chunk vectors with their metadata, and searching by
    similarity. This is the only place in the app that talks to
    Qdrant directly, same principle as SQL repositories for SQLite.
    """

    # def __init__(self):
    #     self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    #     self.collection_name = settings.QDRANT_COLLECTION_NAME
    def __init__(self):
            self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY, timeout=60)
            self.collection_name = settings.QDRANT_COLLECTION_NAME

    def ensure_collection(self) -> None:
        """Creates the Qdrant collection if it doesn't already exist. Safe to call every startup."""
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=settings.EMBEDDING_DIMENSION, distance=Distance.COSINE),
            )

    # def upsert_chunks(
    #     self, chunk_ids: list[int], vectors: list[list[float]], payloads: list[dict]
    # ) -> list[str]:
    #     """
    #     Stores vectors in Qdrant, one per chunk. Returns the generated
    #     Qdrant point IDs, so callers can save them back onto the
    #     SQLite DocumentChunk rows (via vector_id).
    #     """
    #     point_ids = [str(uuid.uuid4()) for _ in chunk_ids]
    #     points = [
    #         PointStruct(id=point_id, vector=vector, payload=payload)
    #         for point_id, vector, payload in zip(point_ids, vectors, payloads)
    #     ]
    #     self.client.upsert(collection_name=self.collection_name, points=points)
    #     return point_ids

    def upsert_chunks(
            self, chunk_ids: list[int], vectors: list[list[float]], payloads: list[dict]
        ) -> list[str]:
            """
            Stores vectors in Qdrant, one per chunk, in smaller batches with
            retries — avoids timeouts on slower/local Qdrant instances when
            upserting many points at once.
            """
            import time

            point_ids = [str(uuid.uuid4()) for _ in chunk_ids]
            points = [
                PointStruct(id=point_id, vector=vector, payload=payload)
                for point_id, vector, payload in zip(point_ids, vectors, payloads)
            ]

            BATCH_SIZE = 50
            MAX_RETRIES = 3

            for i in range(0, len(points), BATCH_SIZE):
                batch = points[i:i + BATCH_SIZE]
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        self.client.upsert(collection_name=self.collection_name, points=batch)
                        break
                    except Exception as e:
                        if attempt == MAX_RETRIES:
                            raise
                        time.sleep(attempt * 3)

            return point_ids

    def search(self, query_vector: list[float], top_k: int = 5, companies: list[str] | None = None) -> list[dict]:
        """Finds the top_k most similar vectors, optionally filtered to specific companies."""
        query_filter = None
        if companies:
            query_filter = Filter(
                must=[FieldCondition(key="company", match=MatchAny(any=companies))]
            )

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=query_filter,
        )
        return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]