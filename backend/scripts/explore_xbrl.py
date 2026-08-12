from app.services.validation.xbrl_client import XbrlClient

client = XbrlClient()

AAPL_CIK = "0000320193"
facts = client.get_tracked_facts(AAPL_CIK)

for label, values in facts.items():
    print(f"\n=== {label} ===")
    for v in values[-5:]:  # show the 5 most recent entries
        print(f"  FY end {v.get('end')}: ${v.get('val'):,} (filed {v.get('filed')})")