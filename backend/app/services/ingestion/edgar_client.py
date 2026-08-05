import time
from pathlib import Path
from typing import Any

import requests

from app.core.config import get_settings

settings = get_settings()

EDGAR_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
EDGAR_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"

# SEC requires a descriptive User-Agent on every request, or it returns 403.
# SEC also asks that automated requests stay under 10 requests/second —
# we're nowhere near that, but we still add a small delay to be a good citizen.
HEADERS = {"User-Agent": settings.SEC_EDGAR_USER_AGENT}
REQUEST_DELAY_SECONDS = 0.3


class EdgarClient:
    """
    Thin client for SEC EDGAR's public JSON API.
    Handles: looking up a company's filing history, filtering to 10-Ks,
    and downloading the actual filing HTML document.
    """

    def get_filing_history(self, cik: str) -> dict[str, Any]:
        """Fetch full submission history (all form types) for a given CIK."""
        url = EDGAR_SUBMISSIONS_URL.format(cik=cik)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)
        return response.json()

    def get_10k_filings(self, cik: str, num_years: int = 3) -> list[dict[str, Any]]:
        """
        Return metadata for the most recent `num_years` 10-K filings for this CIK.
        Each entry includes accession number, filing date, and primary document filename —
        everything needed to construct the download URL.
        """
        data = self.get_filing_history(cik)
        recent = data["filings"]["recent"]

        results = []
        for i, form in enumerate(recent["form"]):
            if form == "10-K":
                results.append(
                    {
                        "accession_number": recent["accessionNumber"][i],
                        "filing_date": recent["filingDate"][i],
                        "primary_document": recent["primaryDocument"][i],
                    }
                )
            if len(results) >= num_years:
                break

        return results

    def download_filing_html(self, cik: str, accession_number: str, primary_document: str, save_path: Path) -> Path:
        """
        Downloads the actual 10-K HTML document to disk.
        `accession_number` has dashes in the API response (e.g. '0000320193-23-000106')
        but the archive URL needs them removed.
        """
        accession_no_dashes = accession_number.replace("-", "")
        url = f"{EDGAR_ARCHIVES_BASE}/{int(cik)}/{accession_no_dashes}/{primary_document}"

        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)

        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(response.content)
        return save_path