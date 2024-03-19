import uuid
from fastapi import FastAPI
from app.db import dogs_facts_api
from app import schemas
from datetime import datetime

app = FastAPI()


@app.post(
    "/api/v1/facts/",
    response_model=schemas.FactsResponse,
    status_code=201,
)
def post_fact(fact: schemas.PostFactsRequest):
    fact_id = str(uuid.uuid4())
    created_at = str(datetime.now())
    fact = {'fact_id': fact_id,
            'fact_text': fact.fact_text,
            'interest': fact.interest,
            'likes': fact.likes,
            'created_at': created_at}
    dogs_facts_api.add_fact(fact)
    return schemas.FactsResponse(
        id=fact["fact_id"],
        fact_text=fact["fact_text"],
        interest=fact["interest"],
        likes=fact["likes"],
        created_at=fact["created_at"],
    )


@app.get("/api/v1/facts", status_code=200)
def get_facts():
    return dogs_facts_api.get_facts()
