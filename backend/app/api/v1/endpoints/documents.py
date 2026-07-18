"""
Documents Endpoint Router for sec-rag.

Exposes thin routes for uploading filings, checking processing status,
and listing indexed documents.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.document import DocumentResponse, DocumentCreate
from app.repositories.document_repository import SQLDocumentRepository
from app.services.parsing.service import ParsingService

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Upload a new SEC Filing document and start async parsing, chunking, and embedding pipelines.
    """
    # TODO: Stream and save file under data/raw_filings/
    # TODO: Register document with status 'pending' in SQLDocumentRepository
    # TODO: Trigger batch processing or queue background task
    repo = SQLDocumentRepository(db)
    doc_in = DocumentCreate(
        filename=file.filename or "unknown.txt",
        file_path=f"data/raw_filings/{file.filename or 'unknown.txt'}",
        ticker="MOCK",
        form_type="10-K",
        filing_date=None
    )
    doc = await repo.create_document(doc_in)
    return doc


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve list of uploaded filings with pagination.
    """
    repo = SQLDocumentRepository(db)
    documents = await repo.list_documents(skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve processing details, status, and chunks of a specific document.
    """
    repo = SQLDocumentRepository(db)
    doc = await repo.get_document(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return doc
