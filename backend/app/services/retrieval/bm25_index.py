from rank_bm25 import BM25Okapi

from app.models.chunk import DocumentChunk


class BM25Index:
    def __init__(self, chunks: list[DocumentChunk]):
        self.chunks = chunks
        tokenized_corpus = [self._tokenize(chunk.content) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def _tokenize(self, text: str) -> list[str]:
        return text.lower().split()

    def search(self, query: str, top_k: int = 5, companies: list[str] | None = None) -> list[tuple[DocumentChunk, float]]:
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        scored_chunks = list(zip(self.chunks, scores))
        if companies:
            scored_chunks = [(chunk, score) for chunk, score in scored_chunks if chunk.company in companies]

        scored_chunks.sort(key=lambda pair: pair[1], reverse=True)
        return scored_chunks[:top_k]