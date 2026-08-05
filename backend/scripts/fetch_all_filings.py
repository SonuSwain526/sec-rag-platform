"""
Fetches the last 3 years of 10-K filings for all companies in scope,
saving each as raw HTML to data/raw_filings/.
Run once (or re-run anytime) to (re)populate your local filing dataset.
"""
from pathlib import Path

from app.services.ingestion.companies import COMPANIES
from app.services.ingestion.edgar_client import EdgarClient

client = EdgarClient()
RAW_FILINGS_DIR = Path("data/raw_filings")


def main() -> None:
    for ticker, cik in COMPANIES.items():
        print(f"\n=== {ticker} ===")
        filings = client.get_10k_filings(cik, num_years=3)

        if not filings:
            print(f"  WARNING: no 10-K filings found for {ticker}")
            continue

        for filing in filings:
            save_path = RAW_FILINGS_DIR / f"{ticker.lower()}_{filing['filing_date']}.htm"

            if save_path.exists():
                print(f"  Skipping (already downloaded): {save_path.name}")
                continue

            result_path = client.download_filing_html(
                cik=cik,
                accession_number=filing["accession_number"],
                primary_document=filing["primary_document"],
                save_path=save_path,
            )
            size_kb = result_path.stat().st_size / 1024
            print(f"  Saved: {result_path.name} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()