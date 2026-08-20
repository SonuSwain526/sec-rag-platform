from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository
from app.services.retrieval.bm25_index import BM25Index

RRF_K = 60


class HybridSearch:
    def __init__(self, embedder: Embedder, vector_repo: VectorRepository, bm25_index: BM25Index):
        self.embedder = embedder
        self.vector_repo = vector_repo
        self.bm25_index = bm25_index

    def search(self, query: str, top_k: int = 5, candidates_per_method: int = 20, companies: list[str] | None = None) -> list[dict]:
        query_vector = self.embedder.embed_text(query)
        semantic_results = self.vector_repo.search(query_vector, top_k=candidates_per_method, companies=companies)
        bm25_results = self.bm25_index.search(query, top_k=candidates_per_method, companies=companies)

        rrf_scores: dict[int, float] = {}
        content_by_chunk_id: dict[int, dict] = {}

        for rank, result in enumerate(semantic_results):
            chunk_id = result["payload"]["sqlite_chunk_id"]
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (RRF_K + rank + 1)
            content_by_chunk_id[chunk_id] = result["payload"]

        for rank, (chunk, _score) in enumerate(bm25_results):
            rrf_scores[chunk.id] = rrf_scores.get(chunk.id, 0) + 1 / (RRF_K + rank + 1)
            if chunk.id not in content_by_chunk_id:
                content_by_chunk_id[chunk.id] = {
                    "company": chunk.company,
                    "fiscal_year": chunk.fiscal_year,
                    "item_code": chunk.item_code,
                    "item_title": chunk.item_title,
                    "chunk_type": chunk.chunk_type,
                    "content": chunk.content,
                    "sqlite_chunk_id": chunk.id,
                }

        ranked_chunk_ids = sorted(rrf_scores.items(), key=lambda pair: pair[1], reverse=True)[:top_k]

        return [
            {"rrf_score": score, **content_by_chunk_id[chunk_id]}
            for chunk_id, score in ranked_chunk_ids
        ]