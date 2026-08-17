import os
os.environ["HF_HUB_OFFLINE"] = "0"  # keep online capability, but...

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

settings = get_settings()


import torch

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.model.half()  # use fp16 — roughly halves memory usage

    def embed_text(self, text: str) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        return vectors.tolist()