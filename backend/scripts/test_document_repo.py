"""
One-off manual verification script — not part of the app itself.
Proves the repository can actually create and retrieve rows.
Delete or ignore once you're confident this all works.
"""
from app.db.session import SessionLocal
from app.repositories.document_repository import DocumentRepository

db = SessionLocal()
repo = DocumentRepository(db)

# Create a test record
doc = repo.create(
    company="AAPL",
    fiscal_year=2023,
    filename="aapl_10k_2023.pdf",
    file_path="/data/raw_filings/aapl_10k_2023.pdf",
)
print("Created:", doc.id, doc.company, doc.fiscal_year, doc.status)

# Fetch it back
fetched = repo.get_by_id(doc.id)
print("Fetched:", fetched.id, fetched.filename)

# Update status
updated = repo.update_status(doc.id, "parsing")
print("Updated status:", updated.status)

# List by company
results = repo.list_by_company("AAPL")
print("Documents for AAPL:", [d.filename for d in results])

db.close()