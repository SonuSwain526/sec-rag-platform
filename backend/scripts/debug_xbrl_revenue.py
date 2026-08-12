from app.services.validation.xbrl_client import XbrlClient

client = XbrlClient()
AAPL_CIK = "0000320193"

data = client.get_company_facts(AAPL_CIK)
revenues = data["facts"]["us-gaap"]["Revenues"]["units"]["USD"]

# Show ALL raw fields for entries where 'form' is 10-K, so we can see
# what actually distinguishes annual figures from quarterly ones
tenk_entries = [v for v in revenues if v.get("form") == "10-K"]

print(f"Total 10-K-tagged entries: {len(tenk_entries)}\n")
for v in tenk_entries[:15]:
    print(v)