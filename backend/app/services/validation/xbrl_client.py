import time
from typing import Any
from datetime import datetime
import requests

from app.core.config import get_settings

settings = get_settings()

XBRL_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
HEADERS = {"User-Agent": settings.SEC_EDGAR_USER_AGENT}
REQUEST_DELAY_SECONDS = 0.3

# The specific XBRL "concept" tags we care about, mapped to a readable label.
# These are standardized US-GAAP taxonomy names — the same across all filers.
TRACKED_CONCEPTS = {
    "RevenueFromContractWithCustomerExcludingAssessedTax": "Total Revenue",
    "Revenues": "Total Revenue",  # fallback for companies/years still using the older tag
    "NetIncomeLoss": "Net Income",
    "ResearchAndDevelopmentExpense": "R&D Expense",
}

class XbrlClient:
    """
    Fetches structured XBRL financial facts from SEC's official API —
    used as independent ground truth to verify numbers our RAG system
    extracts from unstructured 10-K text.
    """

    def get_company_facts(self, cik: str) -> dict[str, Any]:
        url = XBRL_FACTS_URL.format(cik=cik)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)
        return response.json()
    def get_tracked_facts(self, cik: str) -> dict[str, list[dict]]:
            data = self.get_company_facts(cik)
            us_gaap_facts = data.get("facts", {}).get("us-gaap", {})

            results: dict[str, list[dict]] = {}
            for concept, label in TRACKED_CONCEPTS.items():
                if concept not in us_gaap_facts:
                    continue
                usd_values = us_gaap_facts[concept].get("units", {}).get("USD", [])
                annual_values = [v for v in usd_values if self._is_full_year(v)]

                # Merge into any existing entries for this label (multiple XBRL
                # tags can map to the same label, e.g. old vs new revenue tags)
                results.setdefault(label, []).extend(annual_values)

            # Dedupe AFTER merging all concepts for each label, so the most
            # recently filed entry wins regardless of which tag it came from
            for label in results:
                results[label] = self._dedupe_by_period(results[label])

            return results
    def _is_full_year(self, entry: dict) -> bool:
        """True if this entry represents a full fiscal year, not a quarter."""
        if entry.get("form") != "10-K":
            return False

        frame = entry.get("frame", "")
        if "Q" in frame:  # e.g. "CY2018Q3" — a quarter, reject
            return False

        start = entry.get("start")
        end = entry.get("end")
        if not start or not end:
            return False

        days = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).days
        return 350 <= days <= 380  # roughly a year, allowing for 52/53-week fiscal years

    def _dedupe_by_period(self, entries: list[dict]) -> list[dict]:
        """
        The same fiscal year sometimes appears multiple times (reported
        again as a comparison figure in a LATER filing). Keep only the
        most recently filed entry per unique period end date.
        """
        by_end_date: dict[str, dict] = {}
        for entry in entries:
            end = entry["end"]
            if end not in by_end_date or entry["filed"] > by_end_date[end]["filed"]:
                by_end_date[end] = entry
        return sorted(by_end_date.values(), key=lambda e: e["end"])