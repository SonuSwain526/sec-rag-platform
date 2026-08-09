from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository
from app.services.retrieval.bm25_index import BM25Index
from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker
from app.services.retrieval.pipeline import RetrievalPipeline

print("Loading chunks and building indexes...")
db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()

embedder = Embedder()
vector_repo = VectorRepository()
bm25_index = BM25Index(all_chunks)
hybrid = HybridSearch(embedder, vector_repo, bm25_index)

print("Loading reranker model (bge-reranker-large)...")
reranker = Reranker()

pipeline = RetrievalPipeline(hybrid, reranker)

query = "What was Apple's total revenue?"

print(f"\n{'='*70}\nBEFORE reranking (hybrid search only, top 5)\n{'='*70}")
before = hybrid.search(query, top_k=5)
for i, r in enumerate(before, 1):
    print(f"[{i}] {r['company']} FY{r['fiscal_year']} | Item {r['item_code']}: {r['content'][:150]}")

print(f"\n{'='*70}\nAFTER reranking (top 5)\n{'='*70}")
after = pipeline.retrieve(query, final_top_k=5)
for i, r in enumerate(after, 1):
    print(f"[{i}] rerank_score={r['rerank_score']:.4f} | {r['company']} FY{r['fiscal_year']} | Item {r['item_code']}: {r['content'][:150]}")

db.close()