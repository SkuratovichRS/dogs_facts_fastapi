import uuid
from fastapi import FastAPI, HTTPException
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
        fact_id=fact["fact_id"],
        fact_text=fact["fact_text"],
        interest=fact["interest"],
        likes=fact["likes"],
        created_at=fact["created_at"],
    )


@app.get("/api/v1/facts/",
         response_model=schemas.GetFactsResponse,
         status_code=200)
def get_facts(page: int = 0, page_size: int = 5, sorting: str = 'likes'):
    return schemas.GetFactsResponse(total=dogs_facts_api.total(),
                                    data=dogs_facts_api.get_facts(page, page_size, sorting))


@app.get("/api/v1/facts/<id>",
         response_model=schemas.FactsResponse, status_code=200)
def get_fact_by_id(fact_id: str):
    if not dogs_facts_api.get_fact_by_id(fact_id):
        raise HTTPException(status_code=404, detail=f"Fact {fact_id} is not found")
    return dogs_facts_api.get_fact_by_id(fact_id)


@app.delete('/api/v1/facts/<id>',
            status_code=204)
def delete_fact_by_id(fact_id: str):
    dogs_facts_api.delete_fact_by_id(fact_id)


@app.put('/api/v1/facts/<id>',
         response_model=schemas.FactsResponse, status_code=201)
def change_fact_by_id(fact_id: str, fact_text: str = None,
                      interest: int = None, likes: int = None):
    if not dogs_facts_api.change_fact_by_id(fact_id):
        raise HTTPException(status_code=404, detail=f"Fact {fact_id} is not found")
    return dogs_facts_api.change_fact_by_id(fact_id, fact_text, interest, likes)


@app.post('/api/v1/facts/<id>/like',
          response_model=schemas.FactsResponse, status_code=201)
def add_like_by_id(fact_id: str):
    if not dogs_facts_api.add_like_by_id(fact_id):
        raise HTTPException(status_code=404, detail=f"Fact {fact_id} is not found")
    return dogs_facts_api.add_like_by_id(fact_id)


@app.post('/api/v1/facts/import',
          response_model=schemas.ImportFactsResponse, status_code=201)
def import_facts_from_dogapi(amount: int):
    dogs_facts_api.import_facts_from_dogapi(amount)
    return schemas.ImportFactsResponse(amount=amount)
