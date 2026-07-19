from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    """
    Encapsulates all database access for the Document model.
    Services and API endpoints should go through this class instead
    of writing raw SQLAlchemy queries directly — keeps DB access logic
    in one place, and makes services easy to unit test (mock this class
    instead of needing a real database).
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        company: str,
        fiscal_year: int,
        filename: str,
        file_path: str,
    ) -> Document:
        """Insert a new Document record with status='pending'."""
        document = Document(
            company=company,
            fiscal_year=fiscal_year,
            filename=filename,
            file_path=file_path,
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)  # populates auto-generated fields (id, created_at)
        return document

    def get_by_id(self, document_id: int) -> Document | None:
        """Fetch a single Document by its primary key, or None if not found."""
        return self.db.get(Document, document_id)

    def list_all(self) -> list[Document]:
        """Return all Document records. Fine for now; add pagination once volume grows."""
        return self.db.query(Document).all()

    def list_by_company(self, company: str) -> list[Document]:
        """Return all filings for a given company ticker."""
        return self.db.query(Document).filter(Document.company == company).all()

    def update_status(self, document_id: int, status: str) -> Document | None:
        """Update a document's pipeline status (pending/parsing/chunked/embedded/ready/failed)."""
        document = self.get_by_id(document_id)
        if document is None:
            return None
        document.status = status
        self.db.commit()
        self.db.refresh(document)
        return document