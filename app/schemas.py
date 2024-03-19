import uuid

from pydantic import BaseModel


class PostFactsRequest(BaseModel):
    fact_text: str
    interest: int
    likes: int = 0


class FactsResponse(PostFactsRequest):
    id: uuid.UUID
