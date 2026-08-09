from rank_bm25 import BM25Okapi

from app.models.chunk import DocumentChunk


class BM25Index:
    """
    In-memory BM25 keyword search index, built from chunk text.
    Unlike Qdrant (which persists vectors permanently), this index is
    lightweight enough to rebuild fresh each time the app starts —
    no separate storage needed.
    """

    def __init__(self, chunks: list[DocumentChunk]):
        self.chunks = chunks
        tokenized_corpus = [self._tokenize(chunk.content) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def _tokenize(self, text: str) -> list[str]:
        """Simple lowercase whitespace tokenization — good enough for BM25's needs."""
        return text.lower().split()

    def search(self, query: str, top_k: int = 5) -> list[tuple[DocumentChunk, float]]:
        """Returns the top_k chunks most relevant to the query by keyword match, with their BM25 scores."""
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        scored_chunks = list(zip(self.chunks, scores))
        scored_chunks.sort(key=lambda pair: pair[1], reverse=True)

        return scored_chunks[:top_k]