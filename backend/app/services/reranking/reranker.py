from sentence_transformers import CrossEncoder

from app.core.config import get_settings

settings = get_settings()


class Reranker:
    """
    Wraps BAAI/bge-reranker-large — a cross-encoder that scores how well
    a specific chunk answers a specific query, more precisely than
    embedding similarity alone. Used as a second-stage refinement on
    top of hybrid search's already-narrowed candidate list, since
    cross-encoders are too slow to run against the full chunk set.
    """

    def __init__(self):
        self.model = CrossEncoder(settings.RERANKER_MODEL_NAME)

    def rerank(self, query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
        """
        Re-scores and reorders candidates by true relevance to the query.
        Each candidate dict must have a 'content' key (the chunk text).
        Adds a 'rerank_score' key to each returned candidate.
        """
        if not candidates:
            return []

        pairs = [(query, candidate["content"]) for candidate in candidates]
        scores = self.model.predict(pairs)

        for candidate, score in zip(candidates, scores):
            candidate["rerank_score"] = float(score)

        reranked = sorted(candidates, key=lambda c: c["rerank_score"], reverse=True)
        return reranked[:top_k]