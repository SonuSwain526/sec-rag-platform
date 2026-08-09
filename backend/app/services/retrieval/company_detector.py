COMPANY_ALIASES = {
        "AAPL": [
            "apple", "aapl", "iphone", "ipad", "mac", "macbook", "ios", 
            "tim cook", "steve jobs", "app store", "airpods", "apple watch"
        ],
        "MSFT": [
            "microsoft", "msft", "windows", "azure", "office365", "xbox", 
            "satya nadella", "bill gates", "copilot", "teams", "surface"
        ],
        "GOOGL": [
            "google", "alphabet", "googl", "goog", "youtube", "android", 
            "sundar pichai", "larry page", "sergey brin", "gemini", "deepmind", "pixel"
        ],
        "AMZN": [
            "amazon", "amzn", "aws", "prime", "jeff bezos", "andy jassy", 
            "alexa", "kindle", "audible"
        ],
        "META": [
            "meta", "facebook", "fb", "instagram", "insta", "whatsapp", 
            "threads", "oculus", "quest", "mark zuckerberg", "zuck"
        ],
        "NVDA": [
            "nvidia", "nvda", "cuda", "geforce", "rtx", "jensen huang", "jensen"
        ],
        "TSLA": [
            "tesla", "tsla", "elon musk", "musk", "cybertruck", "model 3", "model y"
        ]
}


class CompanyDetector:
    """
    Detects which company ticker(s) are mentioned in a question, using
    simple keyword matching against known aliases. Returns an empty
    list if no company is mentioned (meaning: search everything).
    """

    def detect(self, question: str) -> list[str]:
        question_lower = question.lower()
        detected = []
        for ticker, aliases in COMPANY_ALIASES.items():
            if any(alias in question_lower for alias in aliases):
                detected.append(ticker)
        return detected