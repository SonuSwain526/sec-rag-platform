from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

settings = get_settings()


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        return vectors.tolist()