from fastapi import APIRouter, Depends

from app.schemas.query import QueryRequest, QueryResponse
from app.core.rag_dependencies import get_rag_service
from app.services.generation.rag_service import RagService
from app.api.v1.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    rag_service: RagService = Depends(get_rag_service),
    current_user: User = Depends(get_current_user),
):
    """
    Answers a question about SEC filings using the full RAG pipeline.
    Requires authentication — only logged-in users can query.
    """
    result = rag_service.answer(request.question, verify=request.verify)
    return result