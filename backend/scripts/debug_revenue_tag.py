from app.services.validation.xbrl_client import XbrlClient

client = XbrlClient()
AAPL_CIK = "0000320193"

data = client.get_company_facts(AAPL_CIK)
us_gaap_concepts = data["facts"]["us-gaap"]

# Search for any concept with "Revenue" in its name — to find what Apple
# actually uses for their current revenue reporting
revenue_related = [key for key in us_gaap_concepts.keys() if "revenue" in key.lower()]
print("Revenue-related concepts found in Apple's XBRL data:")
for concept in revenue_related:
    print(f"  - {concept}")