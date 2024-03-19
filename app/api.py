import uuid
from fastapi import FastAPI
from app.main import dogs_facts_api
from app.schemas import AddFacts
from datetime import datetime

app = FastAPI()


@app.post("/api/v1/facts/", status_code=201)
def post_fact(fact: AddFacts) -> dict:
    fact_id = str(uuid.uuid4())
    created_at = str(datetime.now())
    response = {'fact_id': fact_id,
                'fact_text': fact.fact_text,
                'interest': fact.interest,
                'likes': fact.likes,
                'created_at': created_at}
    dogs_facts_api.add_fact(response)
    return response


@app.get("/api/v1/facts", status_code=200)
def get_facts():
    return dogs_facts_api.get_facts()
