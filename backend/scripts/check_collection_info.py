from qdrant_client import QdrantClient

from app.core.config import get_settings

settings = get_settings()

print(f"QDRANT_URL from .env: {settings.QDRANT_URL}")

client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
print(f"Collection vector size: {info.config.params.vectors.size}")
print(f"Points count: {client.count(settings.QDRANT_COLLECTION_NAME).count}")