from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType

from app.core.config import get_settings

settings = get_settings()

client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

client.create_payload_index(
    collection_name=settings.QDRANT_COLLECTION_NAME,
    field_name="company",
    field_schema=PayloadSchemaType.KEYWORD,
)
print(f"Payload index on 'company' created for collection '{settings.QDRANT_COLLECTION_NAME}'.")