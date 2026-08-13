from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    verify: bool = False


class SourceInfo(BaseModel):
    company: str
    fiscal_year: int
    item_code: str
    item_title: str


class VerificationResult(BaseModel):
    company: str | None = None
    fiscal_year: int | None = None
    metric: str | None = None
    value: float | None = None
    status: str
    xbrl_value: float | None = None
    percent_diff: float | None = None
    reason: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
    verification: list[VerificationResult] | None = None