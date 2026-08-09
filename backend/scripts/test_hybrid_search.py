from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository
from app.services.retrieval.bm25_index import BM25Index
from app.services.retrieval.hybrid_search import HybridSearch

print("Loading all chunks from database...")
db = SessionLocal()
all_chunks = db.query(DocumentChunk).all()
print(f"Loaded {len(all_chunks)} chunks total.")

print("Loading embedding model...")
embedder = Embedder()

vector_repo = VectorRepository()

print("Building BM25 index...")
bm25_index = BM25Index(all_chunks)

hybrid = HybridSearch(embedder, vector_repo, bm25_index)

queries = [
    "What was Apple's total revenue?",
    "Microsoft cloud computing risk factors",
    "Amazon employee headcount",
]

for query in queries:
    print(f"\n{'='*70}\nQuery: {query}\n{'='*70}")
    results = hybrid.search(query, top_k=3)
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] RRF Score: {r['rrf_score']:.4f} | {r['company']} FY{r['fiscal_year']} | Item {r['item_code']} ({r['item_title'][:40]})")
        print(r["content"][:250])

db.close()