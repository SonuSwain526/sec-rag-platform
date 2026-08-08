from app.services.embedding.embedder import Embedder
from app.repositories.vector_repository import VectorRepository

print("Loading embedding model...")
embedder = Embedder()

vector_repo = VectorRepository()

query = "What products does Apple sell?"
print(f"\nQuery: {query}")

query_vector = embedder.embed_text(query)
results = vector_repo.search(query_vector, top_k=3)

print(f"\n--- Top {len(results)} results ---\n")
for i, result in enumerate(results, 1):
    payload = result["payload"]
    print(f"[{i}] Score: {result['score']:.4f} | Item {payload['item_code']} ({payload['item_title'][:40]})")
    print(payload["content"][:300])
    print("---")