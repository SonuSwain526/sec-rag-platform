from qdrant_client import QdrantClient

from app.core.config import get_settings

settings = get_settings()

print("=== LOCAL Qdrant (localhost:6333) ===")
try:
    local_client = QdrantClient(url="http://localhost:6333")
    local_info = local_client.get_collection(settings.QDRANT_COLLECTION_NAME)
    print(f"Vector size: {local_info.config.params.vectors.size}")
    print(f"Points count: {local_client.count(settings.QDRANT_COLLECTION_NAME).count}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== CLOUD Qdrant (from .env) ===")
print(f"URL: {settings.QDRANT_URL}")
cloud_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
cloud_info = cloud_client.get_collection(settings.QDRANT_COLLECTION_NAME)
print(f"Vector size: {cloud_info.config.params.vectors.size}")
print(f"Points count: {cloud_client.count(settings.QDRANT_COLLECTION_NAME).count}")

print(f"\n=== Current .env EMBEDDING_DIMENSION setting ===")
print(f"{settings.EMBEDDING_DIMENSION}")