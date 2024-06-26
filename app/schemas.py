import uuid
from datetime import datetime
from pydantic import BaseModel


class PostFactsRequest(BaseModel):
    fact_text: str
    interest: int
    likes: int = 0


class FactsResponse(PostFactsRequest):
    fact_id: uuid.UUID
    created_at: datetime


class GetFactsResponse(BaseModel):
    total: int
    data: list[FactsResponse]


class ImportFactsResponse(BaseModel):
    amount: int

