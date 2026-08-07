from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.services.chunking.models import Chunk as ChunkDTO


class ChunkRepository:
    """
    Encapsulates database access for DocumentChunk records.
    Takes chunking output (Chunk dataclasses) and persists them,
    linked to their parent Document.
    """

    def __init__(self, db: Session):
        self.db = db

    def save_chunks(self, document_id: int, chunks: list[ChunkDTO]) -> list[DocumentChunk]:
        """Bulk-saves a list of chunk objects, linked to the given document."""
        db_chunks = [
            DocumentChunk(
                document_id=document_id,
                company=chunk.company,
                fiscal_year=chunk.fiscal_year,
                item_code=chunk.item_code,
                item_title=chunk.item_title,
                chunk_type=chunk.chunk_type,
                content=chunk.content,
                token_count=chunk.token_count,
            )
            for chunk in chunks
        ]
        self.db.add_all(db_chunks)
        self.db.commit()
        for c in db_chunks:
            self.db.refresh(c)
        return db_chunks

    def get_by_document(self, document_id: int) -> list[DocumentChunk]:
        """Returns all chunks belonging to a given document."""
        return self.db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()

    def count_by_document(self, document_id: int) -> int:
        return self.db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()