SYSTEM_PROMPT = """You are a financial research assistant that answers questions about SEC 10-K filings.

Rules you must follow:
1. Answer ONLY using the provided context chunks below. Do not use any outside knowledge.
2. If the context does not contain enough information to answer the question, say so clearly instead of guessing.
3. When you state a fact or number, cite its source in this format: [Company FYYear, Item X].
4. Be precise with numbers — do not round or approximate unless the source itself does.
5. Keep your answer clear and directly focused on the question asked."""


class PromptBuilder:
    """
    Builds the actual prompt sent to the LLM, combining the user's
    question with retrieved, reranked context chunks — this is what
    'grounds' the model's answer in real retrieved evidence instead
    of its own training data.
    """

    def build_user_prompt(self, question: str, chunks: list[dict]) -> str:
        context_blocks = []
        for i, chunk in enumerate(chunks, 1):
            source_tag = f"[{chunk['company']} FY{chunk['fiscal_year']}, Item {chunk['item_code']}: {chunk['item_title']}]"
            context_blocks.append(f"--- Context {i} {source_tag} ---\n{chunk['content']}")

        context_text = "\n\n".join(context_blocks)

        return f"""Context from SEC filings:

{context_text}

Question: {question}

Answer the question using only the context above, citing sources as instructed."""