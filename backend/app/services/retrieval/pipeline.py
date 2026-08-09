from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker


class RetrievalPipeline:
    """
    Full retrieval pipeline: hybrid search narrows the whole chunk set
    down to a candidate shortlist, then the reranker precisely re-scores
    and reorders that shortlist for final use.
    """

    def __init__(self, hybrid_search: HybridSearch, reranker: Reranker):
        self.hybrid_search = hybrid_search
        self.reranker = reranker

    def retrieve(self, query: str, final_top_k: int = 5, candidate_pool_size: int = 15) -> list[dict]:
        candidates = self.hybrid_search.search(query, top_k=candidate_pool_size)
        return self.reranker.rerank(query, candidates, top_k=final_top_k)