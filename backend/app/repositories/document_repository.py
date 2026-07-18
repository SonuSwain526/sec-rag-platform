"""
Document Repository Module for sec-rag.

Exposes interfaces and implementations for PostgreSQL document table data operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentChunk
from app.schemas.document import DocumentCreate


class BaseDocumentRepository(ABC):
    """
    Abstract interface for managing Document and DocumentChunk database persistence.
    """
    @abstractmethod
    async def create_document(self, doc_in: DocumentCreate) -> Document:
        """Persist a new document record."""
        pass

    @abstractmethod
    async def get_document(self, doc_id: int) -> Optional[Document]:
        """Fetch a document record by ID."""
        pass

    @abstractmethod
    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """List document records with pagination."""
        pass

    @abstractmethod
    async def update_document_status(self, doc_id: int, status: str) -> Optional[Document]:
        """Update processing status of a document."""
        pass

    @abstractmethod
    async def add_document_chunks(self, doc_id: int, chunks: List[dict]) -> List[DocumentChunk]:
        """Persist chunk blocks for a parsed document."""
        pass


class SQLDocumentRepository(BaseDocumentRepository):
    """
    SQLAlchemy-backed async repository for PostgreSQL databases.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_document(self, doc_in: DocumentCreate) -> Document:
        """
        Creates and stores a Document entity.
        """
        db_doc = Document(
            filename=doc_in.filename,
            file_path=doc_in.file_path,
            ticker=doc_in.ticker,
            form_type=doc_in.form_type,
            filing_date=doc_in.filing_date,
            status="pending"
        )
        self.db.add(db_doc)
        await self.db.commit()
        await self.db.refresh(db_doc)
        return db_doc

    async def get_document(self, doc_id: int) -> Optional[Document]:
        """
        Fetches a document by its primary key id.
        """
        # TODO: Add joinedload for chunks to prevent N+1 queries if needed
        result = await self.db.execute(select(Document).where(Document.id == doc_id))
        return result.scalars().first()

    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """
        Fetches multiple documents with pagination.
        """
        result = await self.db.execute(select(Document).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_document_status(self, doc_id: int, status: str) -> Optional[Document]:
        """
        Updates the status of a document and commits changes.
        """
        db_doc = await self.get_document(doc_id)
        if db_doc:
            db_doc.status = status
            self.db.add(db_doc)
            await self.db.commit()
            await self.db.refresh(db_doc)
        return db_doc

    async def add_document_chunks(self, doc_id: int, chunks: List[dict]) -> List[DocumentChunk]:
        """
        Adds multiple chunk blocks associated with a document.
        """
        db_chunks = []
        for c in chunks:
            chunk = DocumentChunk(
                document_id=doc_id,
                chunk_index=c["chunk_index"],
                content=c["content"],
                vector_id=c.get("vector_id"),
                chunk_metadata=c.get("chunk_metadata", {})
            )
            self.db.add(chunk)
            db_chunks.append(chunk)
        
        await self.db.commit()
        return db_chunks
