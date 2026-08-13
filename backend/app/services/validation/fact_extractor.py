import json

from app.services.generation.groq_client import GroqClient

EXTRACTION_SYSTEM_PROMPT = """You extract financial figures from text into structured JSON.

Given a piece of text, find every specific financial figure mentioned (revenue, net income, R&D expense, etc.) along with the company and fiscal year it refers to.

Respond ONLY with a JSON array, no other text, in this exact format:
[
  {"company": "AAPL", "fiscal_year": 2025, "metric": "Total Revenue", "value": 416161000000}
]

Rules:
- Convert all values to raw dollar amounts (e.g., "$416,161 million" becomes 416161000000)
- Only include metrics that clearly match one of: Total Revenue, Net Income, R&D Expense
- If no financial figures are found, respond with an empty array: []"""


class FactExtractor:
    """
    Uses the LLM to pull structured numeric claims (company, fiscal year,
    metric, value) out of a free-form generated answer, so they can be
    checked against XBRL ground truth. More robust to varied phrasing
    ("$416B" vs "$416,161 million") than regex pattern matching.
    """

    def __init__(self, groq_client: GroqClient):
        self.groq_client = groq_client

    def extract(self, answer_text: str) -> list[dict]:
        response = self.groq_client.generate(EXTRACTION_SYSTEM_PROMPT, answer_text)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return []