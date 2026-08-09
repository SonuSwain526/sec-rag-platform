from app.db.session import SessionLocal
from app.models.document import Document

db = SessionLocal()
docs = db.query(Document).all()
for d in docs:
    print(d.id, d.company, d.fiscal_year, d.status)
db.close()