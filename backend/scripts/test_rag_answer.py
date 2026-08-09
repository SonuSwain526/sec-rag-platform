from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository
from app.services.retrieval.bm25_index import BM25Index
from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker
from app.services.retrieval.pipeline import RetrievalPipeline
from app.services.generation.groq_client import GroqClient
from app.services.generation.prompt_builder import PromptBuilder
from app.services.generation.rag_service import RagService
from app.services.retrieval.company_detector import CompanyDetector

print("Loading chunks and building indexes...")
db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()

embedder = Embedder()
vector_repo = VectorRepository()
bm25_index = BM25Index(all_chunks)
hybrid = HybridSearch(embedder, vector_repo, bm25_index)

print("Loading reranker...")
reranker = Reranker()
company_detector = CompanyDetector()
pipeline = RetrievalPipeline(hybrid, reranker, company_detector)

groq_client = GroqClient()
prompt_builder = PromptBuilder()
rag_service = RagService(pipeline, groq_client, prompt_builder)

questions = [
    "What was Apple's total revenue in fiscal year 2025?",
    "What are Microsoft's main risk factors related to cloud computing?",
    "What are Microsoft's main risk factors related to cloud computing?",
    "Compare Apple and Microsoft's approach to risk factors.",
]

for question in questions:
    print(f"\n{'='*70}\nQuestion: {question}\n{'='*70}")
    result = rag_service.answer(question)
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources used:")
    for s in result["sources"]:
        print(f"  - {s['company']} FY{s['fiscal_year']}, Item {s['item_code']} ({s['item_title']})")

db.close()