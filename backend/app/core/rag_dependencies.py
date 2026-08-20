from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository
from app.services.retrieval.bm25_index import BM25Index
from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker
from app.services.retrieval.company_detector import CompanyDetector
from app.services.retrieval.pipeline import RetrievalPipeline
from app.services.generation.groq_client import GroqClient
from app.services.generation.prompt_builder import PromptBuilder
from app.services.generation.rag_service import RagService
from app.services.validation.xbrl_client import XbrlClient
from app.services.validation.fact_extractor import FactExtractor
from app.services.validation.validator import XbrlValidator

_rag_service: RagService | None = None


def build_rag_service() -> RagService:
    db = SessionLocal()
    all_chunks = db.query(DocumentChunk).all()
    db.close()

    embedder = Embedder()
    vector_repo = VectorRepository()
    bm25_index = BM25Index(all_chunks)
    hybrid = HybridSearch(embedder, vector_repo, bm25_index)
    reranker = Reranker()
    company_detector = CompanyDetector()
    pipeline = RetrievalPipeline(hybrid, reranker, company_detector)

    groq_client = GroqClient()
    prompt_builder = PromptBuilder()

    xbrl_client = XbrlClient()
    fact_extractor = FactExtractor(groq_client)
    validator = XbrlValidator(xbrl_client, fact_extractor)

    return RagService(pipeline, groq_client, prompt_builder, validator)


def get_rag_service() -> RagService:
    if _rag_service is None:
        raise RuntimeError("RagService not initialized — check app startup/lifespan")
    return _rag_service


def set_rag_service(service: RagService) -> None:
    global _rag_service
    _rag_service = service