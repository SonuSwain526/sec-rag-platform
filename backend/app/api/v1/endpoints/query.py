"""
Query Endpoint Router for sec-rag.

Exposes routing for answering financial search queries using the RAG pipeline.
"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.query import QueryRequest, QueryResponse
from app.repositories.document_repository import SQLDocumentRepository
from app.repositories.vector_repository import QdrantVectorRepository

# Import services
from app.services.embedding.service import EmbeddingService
from app.services.retrieval.service import RetrievalService
from app.services.reranking.service import RerankingService
from app.services.generation.service import GenerationService
from app.services.validation.service import ValidationService
from app.services.evaluation.service import EvaluationService

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_rag_pipeline(
    payload: QueryRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Submit a user query. Conducts vector search, cross-encoder reranking,
    LLM prompt synthesis, output validation, and returns the grounded answer.
    """
    # TODO: Perform Dependency injection of all services
    # Instantiating mock dependencies
    emb_service = EmbeddingService()
    doc_repo = SQLDocumentRepository(db)
    
    # Mocking Qdrant client inject
    vec_repo = QdrantVectorRepository(qdrant_client=None)
    
    ret_service = RetrievalService(
        embedding_service=emb_service,
        vector_repository=vec_repo,
        document_repository=doc_repo
    )
    rerank_service = RerankingService()
    gen_service = GenerationService()
    val_service = ValidationService()
    eval_service = EvaluationService()

    try:
        # 1. Retrieve initial context
        raw_contexts = await ret_service.retrieve_context(
            query=payload.query,
            ticker=payload.ticker,
            form_type=payload.form_type,
            top_k=payload.top_k,
            filters=payload.filters
        )
        
        # 2. Rerank the retrieved contexts
        reranked_contexts = await rerank_service.rerank(
            query=payload.query,
            results=raw_contexts,
            top_n=3
        )
        
        # 3. Generate answer via LLM
        answer = await gen_service.generate_answer(
            query=payload.query,
            contexts=reranked_contexts
        )
        
        # 4. Validate output grounding
        validation = await val_service.validate_answer(
            query=payload.query,
            answer=answer,
            contexts=reranked_contexts
        )
        
        # 5. Evaluate overall performance
        evaluation = await eval_service.evaluate_pipeline(
            query=payload.query,
            answer=answer,
            contexts=reranked_contexts,
            validation_results=validation
        )
        
        # Assemble sources response model
        sources = [
            {
                "document_id": c["document_id"],
                "filename": c["filename"],
                "chunk_index": c["chunk_index"],
                "content": c["content"],
                "score": c["score"]
            }
            for c in reranked_contexts
        ]

        return QueryResponse(
            query=payload.query,
            answer=answer,
            sources=sources,
            metadata={
                "validation": validation,
                "evaluation": evaluation
            }
        )

    except Exception as e:
        # TODO: Handle pipeline domain specific exceptions gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while running the search pipeline: {str(e)}"
        )
