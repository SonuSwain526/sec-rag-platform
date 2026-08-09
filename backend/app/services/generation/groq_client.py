from groq import Groq

from app.core.config import get_settings

settings = get_settings()


class GroqClient:
    """
    Thin wrapper around the Groq API for LLM text generation.
    Kept separate from prompt-building and RAG orchestration logic,
    so the actual API call mechanics stay in one place — if we ever
    swap providers, only this file changes.
    """

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL_NAME

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Sends a system + user prompt pair to Groq, returns the model's text response."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,  # low temperature — we want factual, consistent answers, not creative ones
        )
        return response.choices[0].message.content  