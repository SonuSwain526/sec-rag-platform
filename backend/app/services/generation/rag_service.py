from app.services.retrieval.pipeline import RetrievalPipeline
from app.services.generation.groq_client import GroqClient
from app.services.generation.prompt_builder import PromptBuilder, SYSTEM_PROMPT
from app.services.validation.validator import XbrlValidator

class RagService:
    def __init__(self, retrieval_pipeline, groq_client, prompt_builder, validator: XbrlValidator | None = None):
        self.retrieval_pipeline = retrieval_pipeline
        self.groq_client = groq_client
        self.prompt_builder = prompt_builder
        self.validator = validator

    def answer(self, question: str, top_k: int = 7, verify: bool = False) -> dict:
        chunks = self.retrieval_pipeline.retrieve(question, final_top_k=top_k)

        if not chunks:
            return {"answer": "No relevant information was found in the filings.", "sources": []}

        user_prompt = self.prompt_builder.build_user_prompt(question, chunks)
        answer_text = self.groq_client.generate(SYSTEM_PROMPT, user_prompt)

        result = {
            "answer": answer_text,
            "sources": [
                {"company": c["company"], "fiscal_year": c["fiscal_year"], "item_code": c["item_code"], "item_title": c["item_title"]}
                for c in chunks
            ],
        }

        if verify and self.validator:
            result["verification"] = self.validator.validate_answer(answer_text)

        return result