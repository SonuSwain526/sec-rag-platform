from datetime import datetime, timezone

from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentChunk(Base):
    """
    A single retrievable unit of content (text or table) extracted from
    a Document. Each chunk carries the metadata needed for citations —
    which Item/section it came from — and will later store a reference
    to its embedding vector once Phase 8 generates one.
    """
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False, index=True)

    company: Mapped[str] = mapped_column(String, index=True, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    item_code: Mapped[str] = mapped_column(String, index=True, nullable=False)  # e.g. "7", "7A"
    item_title: Mapped[str] = mapped_column(String, nullable=False)
    chunk_type: Mapped[str] = mapped_column(String, nullable=False)  # "text" | "table"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Populated in Phase 9 once we store this chunk's vector in Qdrant —
    # lets us look up "which Qdrant point does this chunk correspond to"
    vector_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )