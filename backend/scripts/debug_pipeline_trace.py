"""
Traces MSFT's Item 1A chunk through each real pipeline stage
(hybrid search candidates -> reranked results) to find exactly
where it gets dropped, since raw embedding similarity alone
ranks it #1 among MSFT sections.
"""
from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository
from app.services.retrieval.bm25_index import BM25Index
from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker

db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()

embedder = Embedder()
vector_repo = VectorRepository()
bm25_index = BM25Index(all_chunks)
hybrid = HybridSearch(embedder, vector_repo, bm25_index)
reranker = Reranker()

query = "Microsoft cloud computing risk factors"

print("=== Stage 1: Hybrid search candidates (top 15, MSFT only) ===\n")
candidates = hybrid.search(query, top_k=15, companies=["MSFT"])
for i, c in enumerate(candidates, 1):
    marker = " <-- ITEM 1A" if c["item_code"] == "1A" else ""
    print(f"[{i}] rrf={c['rrf_score']:.4f} | Item {c['item_code']}{marker}")

print("\n=== Stage 2: After reranking (top 5) ===\n")
reranked = reranker.rerank(query, candidates, top_k=5)
for i, c in enumerate(reranked, 1):
    marker = " <-- ITEM 1A" if c["item_code"] == "1A" else ""
    print(f"[{i}] rerank_score={c['rerank_score']:.4f} | Item {c['item_code']}{marker}")

db.close()