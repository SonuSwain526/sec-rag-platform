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
from app.services.evaluation.evaluator import RagEvaluator
from app.services.evaluation.test_questions import EVAL_QUESTIONS

print("Setting up full pipeline...")
db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()

embedder = Embedder()
vector_repo = VectorRepository()
bm25_index = BM25Index(all_chunks)
hybrid = HybridSearch(embedder, vector_repo, bm25_index)
reranker = Reranker()
company_detector = CompanyDetector()
pipeline = RetrievalPipeline(hybrid, reranker, company_detector)

groq_client = GroqClient()
prompt_builder = PromptBuilder()
rag_service = RagService(pipeline, groq_client, prompt_builder)

evaluator = RagEvaluator(rag_service)
results = evaluator.run(EVAL_QUESTIONS)

print("\n" + "=" * 60)
print("EVALUATION RESULTS")
print("=" * 60)
print(results)

db.close()