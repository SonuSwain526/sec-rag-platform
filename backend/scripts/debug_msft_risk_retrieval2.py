"""
Compares MSFT Item 1A's similarity score against the chunks that
ARE currently winning (Item 1C, Item 7), to see how close the
competition actually is.
"""
import numpy as np
from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder

db = SessionLocal()
embedder = Embedder()

query = "Microsoft cloud computing risk factors"
query_vector = np.array(embedder.embed_text(query))

for item_code in ["1A", "1C", "7"]:
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.company == "MSFT", DocumentChunk.item_code == item_code)
        .limit(20)
        .all()
    )
    print(f"\n=== Item {item_code}: checking top match among {len(chunks)} chunks ===")

    scored = []
    for chunk in chunks:
        chunk_vector = np.array(embedder.embed_text(chunk.content))
        similarity = np.dot(query_vector, chunk_vector)
        scored.append((similarity, chunk))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    top_score, top_chunk = scored[0]
    print(f"Best similarity: {top_score:.4f}")
    print(top_chunk.content[:200])

db.close()