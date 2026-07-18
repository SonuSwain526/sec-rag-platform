"""
Document Database Models for sec-rag.

Defines the Document and DocumentChunk models representing uploaded/processed SEC filings
and their segmented text units.
"""

from datetime import date
from typing import List, Optional
from sqlalchemy import Date, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Document(Base):
    """
    SQLAlchemy model representing an SEC Filing document.
    """
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, processing, completed, failed
    
    # SEC Filing Meta info
    ticker: Mapped[Optional[str]] = mapped_column(String(10), index=True, nullable=True)
    form_type: Mapped[Optional[str]] = mapped_column(String(20), index=True, nullable=True)  # 10-K, 10-Q, etc.
    filing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    chunks: Mapped[List["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )

    # TODO: Add indices for high-frequency queries on metadata parameters
    
    def __repr__(self) -> str:
        return f"<Document filename={self.filename} status={self.status} form={self.form_type}>"


class DocumentChunk(Base):
    """
    SQLAlchemy model representing a segmented chunk of an SEC Document.
    """
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Reference ID mapping to the item in Vector DB (Qdrant)
    vector_id: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    
    # Key-value JSON metadata block for query-time routing filters
    chunk_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="chunks")

    # TODO: Add compound constraints to prevent duplicate chunking indices per document

    def __repr__(self) -> str:
        return f"<DocumentChunk doc_id={self.document_id} index={self.chunk_index} vector_id={self.vector_id}>"
