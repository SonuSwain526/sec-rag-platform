from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas import evaluate, EvaluationDataset
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig

from app.core.config import get_settings
from app.services.generation.rag_service import RagService

settings = get_settings()


class RagEvaluator:
    def __init__(self, rag_service: RagService):
        self.rag_service = rag_service
        self.judge_llm = LangchainLLMWrapper(
                    ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0)
                )
        self.judge_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model="text-embedding-3-small")
        )
        # Ragas needs an embedding model for AnswerRelevancy — point it at

    def run(self, eval_items: list[dict]):
            print(f"Running {len(eval_items)} questions through the RAG pipeline...")
            rows = []
            for i, item in enumerate(eval_items, 1):
                question = item["question"]
                print(f"  [{i}/{len(eval_items)}] {question}")
                result = self.rag_service.answer(question)
                contexts = self._get_contexts_for_answer(question)
                rows.append({
                    "user_input": question,
                    "response": result["answer"],
                    "retrieved_contexts": contexts,
                    "reference": item["reference"],
                })

            dataset = EvaluationDataset.from_list(rows)

            print("\nRunning Ragas evaluation (this calls the judge LLM multiple times per question)...")
            results = evaluate(
                        dataset=dataset,
                        metrics=[Faithfulness(), AnswerRelevancy(), ContextPrecision()],
                        llm=self.judge_llm,
                        embeddings=self.judge_embeddings,
                        run_config=RunConfig(timeout=60, max_workers=5),
                    )
            return results

    def _get_contexts_for_answer(self, question: str) -> list[str]:
        """Re-runs retrieval to get the raw chunk texts Ragas needs alongside the answer."""
        chunks = self.rag_service.retrieval_pipeline.retrieve(question, final_top_k=5)
        return [c["content"] for c in chunks]