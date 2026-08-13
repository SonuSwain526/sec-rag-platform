from app.services.validation.xbrl_client import XbrlClient
from app.services.validation.fact_extractor import FactExtractor

TOLERANCE_PERCENT = 1.0  # allow up to 1% difference — rounding/reporting-unit variance is normal

COMPANY_CIKS = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "AMZN": "0001018724",
    "META": "0001326801",
}


class XbrlValidator:
    """
    Cross-checks numeric claims extracted from a RAG answer against
    SEC's official XBRL structured data — the project's core trust
    mechanism, verifying the LLM's output against an independent source.
    """

    def __init__(self, xbrl_client: XbrlClient, fact_extractor: FactExtractor):
        self.xbrl_client = xbrl_client
        self.fact_extractor = fact_extractor
        self._facts_cache: dict[str, dict] = {}

    def validate_answer(self, answer_text: str) -> list[dict]:
        claims = self.fact_extractor.extract(answer_text)
        results = []

        for claim in claims:
            result = self._validate_claim(claim)
            results.append(result)

        return results

    def _validate_claim(self, claim: dict) -> dict:
        company = claim.get("company")
        fiscal_year = claim.get("fiscal_year")
        metric = claim.get("metric")
        claimed_value = claim.get("value")

        cik = COMPANY_CIKS.get(company)
        if not cik:
            return {**claim, "status": "unverifiable", "reason": "Unknown company"}

        facts = self._get_facts(cik)
        matching_values = facts.get(metric, [])

        actual_entry = next(
            (v for v in matching_values if self._fiscal_year_matches(v["end"], fiscal_year)), None
        )

        if actual_entry is None:
            return {**claim, "status": "unverifiable", "reason": "No matching XBRL data found for this year/metric"}

        actual_value = actual_entry["val"]
        percent_diff = abs(claimed_value - actual_value) / actual_value * 100

        if percent_diff <= TOLERANCE_PERCENT:
            return {**claim, "status": "verified", "xbrl_value": actual_value}
        else:
            return {
                **claim,
                "status": "discrepancy",
                "xbrl_value": actual_value,
                "percent_diff": round(percent_diff, 2),
            }

    def _get_facts(self, cik: str) -> dict:
        if cik not in self._facts_cache:
            self._facts_cache[cik] = self.xbrl_client.get_tracked_facts(cik)
        return self._facts_cache[cik]

    def _fiscal_year_matches(self, end_date: str, fiscal_year: int) -> bool:
        return end_date.startswith(str(fiscal_year))