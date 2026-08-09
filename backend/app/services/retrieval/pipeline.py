from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker
from app.services.retrieval.company_detector import CompanyDetector


class RetrievalPipeline:
    def __init__(self, hybrid_search: HybridSearch, reranker: Reranker, company_detector: CompanyDetector):
        self.hybrid_search = hybrid_search
        self.reranker = reranker
        self.company_detector = company_detector

    def retrieve(self, query: str, final_top_k: int = 5, candidate_pool_size: int = 15) -> list[dict]:
        companies = self.company_detector.detect(query)
        candidates = self.hybrid_search.search(query, top_k=candidate_pool_size, companies=companies or None)
        return self.reranker.rerank(query, candidates, top_k=final_top_k)