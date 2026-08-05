from dataclasses import dataclass, field


@dataclass
class Chunk:
    """
    A single retrievable unit of content, ready for embedding.
    Carries full metadata so retrieval results can be cited precisely
    (company, fiscal year, and which Item/section it came from).
    """
    chunk_id: str
    company: str
    fiscal_year: int
    item_code: str
    item_title: str
    chunk_type: str  # "text" or "table"
    content: str
    token_count: int