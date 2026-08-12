"""
Diagnoses why MSFT Item 1A (Risk Factors) doesn't surface for
risk-factor questions. Checks two things separately:
1. Does Item 1A content actually exist in our database at all?
2. If it exists, how does it score against the query compared to
   what IS being retrieved?
"""
from app.db.session import SessionLocal
from app.models.chunk import DocumentChunk
from app.services.embedding.embedder import Embedder

db = SessionLocal()

# Step 1: does MSFT Item 1A content even exist in the database?
item_1a_chunks = (
    db.query(DocumentChunk)
    .filter(DocumentChunk.company == "MSFT", DocumentChunk.item_code == "1A")
    .all()
)
print(f"MSFT Item 1A chunks found in database: {len(item_1a_chunks)}")

if not item_1a_chunks:
    print("PROBLEM: No Item 1A content exists for MSFT at all — this is a chunking/tagging bug.")
else:
    print(f"Content exists. Showing first chunk:\n")
    print(item_1a_chunks[0].content[:300])

    # Step 2: how does this chunk score against our query, directly?
    print("\n--- Direct similarity check ---")
    embedder = Embedder()
    query = "Microsoft cloud computing risk factors"
    query_vector = embedder.embed_text(query)

    import numpy as np
    query_vec_np = np.array(query_vector)

    for chunk in item_1a_chunks[:3]:
        chunk_vector = embedder.embed_text(chunk.content)
        chunk_vec_np = np.array(chunk_vector)
        similarity = np.dot(query_vec_np, chunk_vec_np)  # already normalized, so dot product = cosine similarity
        print(f"\nChunk (Item 1A): similarity = {similarity:.4f}")
        print(chunk.content[:200])

db.close()