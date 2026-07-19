from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Document(Base):
    """
    Represents one ingested SEC 10-K filing.
    Populated during Phase 4 (PDF Parsing) when a filing is downloaded
    and processed. `status` tracks where it is in the ingestion pipeline.
    """
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company: Mapped[str] = mapped_column(String, index=True, nullable=False)  # e.g. "AAPL"
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(
        String, default="pending"
    )  # pending | parsing | chunked | embedded | ready | failed
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )