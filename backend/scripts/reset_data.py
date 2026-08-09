from app.db.session import SessionLocal
from app.models.document import Document
from app.models.chunk import DocumentChunk
from app.repositories.vector_repository import VectorRepository

db = SessionLocal()
db.query(DocumentChunk).delete()
db.query(Document).delete()
db.commit()
db.close()
print("Cleared all documents and chunks from SQLite.")

vr = VectorRepository()
vr.client.delete_collection(vr.collection_name)
vr.ensure_collection()
print("Qdrant collection reset.")