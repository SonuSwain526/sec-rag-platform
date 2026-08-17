from rank_bm25 import BM25Okapi

from app.models.chunk import DocumentChunk


class BM25Index:
    """
    In-memory BM25 keyword search index. Stores only tokenized corpus
    statistics plus lightweight (chunk_id, company) references — NOT
    full chunk content — to keep memory usage low. Full content for
    any result is fetched from SQLite afterward, only for the small
    final candidate set, not held redundantly for all ~4,700 chunks.
    """

    def __init__(self, chunks: list[DocumentChunk]):
        self.chunk_ids = [chunk.id for chunk in chunks]
        self.companies = [chunk.company for chunk in chunks]
        tokenized_corpus = [self._tokenize(chunk.content) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        # Note: `chunks` itself is not stored — only what's needed above.

    def _tokenize(self, text: str) -> list[str]:
        return text.lower().split()

    def search(self, query: str, top_k: int = 5, companies: list[str] | None = None) -> list[tuple[int, float]]:
        """Returns the top_k (chunk_id, score) pairs — IDs only, content fetched separately."""
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        scored = list(zip(self.chunk_ids, self.companies, scores))
        if companies:
            scored = [(cid, comp, score) for cid, comp, score in scored if comp in companies]

        scored.sort(key=lambda triple: triple[2], reverse=True)
        return [(cid, score) for cid, _comp, score in scored[:top_k]]