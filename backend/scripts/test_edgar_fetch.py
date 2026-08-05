from pathlib import Path

from app.services.ingestion.edgar_client import EdgarClient

client = EdgarClient()

AAPL_CIK = "0000320193"

filings = client.get_10k_filings(AAPL_CIK, num_years=1)
print("Found filing:", filings)

if filings:
    filing = filings[0]
    save_path = Path("data/raw_filings") / f"aapl_{filing['filing_date']}.htm"
    result_path = client.download_filing_html(
        cik=AAPL_CIK,
        accession_number=filing["accession_number"],
        primary_document=filing["primary_document"],
        save_path=save_path,
    )
    print("Saved to:", result_path)
    print("File size:", result_path.stat().st_size, "bytes")