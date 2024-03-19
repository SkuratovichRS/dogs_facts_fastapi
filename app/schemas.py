from pydantic import BaseModel


class AddFacts(BaseModel):
    fact_text: str
    interest: int
    likes: int = 0
