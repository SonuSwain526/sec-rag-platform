from app.services.retrieval.hybrid_search import HybridSearch
from app.services.reranking.reranker import Reranker
from app.services.retrieval.company_detector import CompanyDetector


class RetrievalPipeline:
    def __init__(self, hybrid_search: HybridSearch, reranker: Reranker, company_detector: CompanyDetector):
        self.hybrid_search = hybrid_search
        self.reranker = reranker
        self.company_detector = company_detector

    def retrieve(self, query: str, final_top_k: int = 7, candidate_pool_size: int = 15) -> list[dict]:
        companies = self.company_detector.detect(query)

        if companies and len(companies) > 1:
            # Multi-company query (e.g. "compare Amazon vs Microsoft risk factors").
            # Retrieving with a single pooled top-k across all companies lets one
            # company's higher-scoring chunks crowd out the others entirely, even
            # though both pass the filter. Instead, retrieve a balanced slice
            # per company and merge — this guarantees every requested company is
            # represented in the candidate pool before reranking narrows it down.
            per_company_k = max(candidate_pool_size // len(companies), 5)
            candidates = []
            seen_chunk_ids = set()
            for company in companies:
                company_candidates = self.hybrid_search.search(
                    query, top_k=per_company_k, companies=[company]
                )
                for candidate in company_candidates:
                    chunk_id = candidate.get("sqlite_chunk_id")
                    if chunk_id not in seen_chunk_ids:
                        seen_chunk_ids.add(chunk_id)
                        candidates.append(candidate)
        else:
            candidates = self.hybrid_search.search(query, top_k=candidate_pool_size, companies=companies or None)

        return self.reranker.rerank(query, candidates, top_k=final_top_k)