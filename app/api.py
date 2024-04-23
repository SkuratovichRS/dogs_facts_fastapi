import uuid
from fastapi import FastAPI, HTTPException, Request, Header
from app.db import dogs_facts_api, NotFoundException
from app import schemas
from datetime import datetime
import time
from app.auth import auth_token

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if 'api/v1' not in str(request.url):
        return await call_next(request)
    print("Запрос пришёл")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Запрос выполнен, {process_time}")
    return response


@app.middleware("http")
async def authorization(request: Request, call_next):
    token = request.headers.get("auth")
    if 'api/v1' in str(request.url):
        if token != auth_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
    response = await call_next(request)
    return response


@app.post(
    "/api/v1/facts/",
    response_model=schemas.FactsResponse,
    status_code=201,
)
def post_fact(fact: schemas.PostFactsRequest, auth: str = Header()):
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
def get_facts(page: int = 0, page_size: int = 5,
              sorting: str = 'likes', auth: str = Header()):
    data, total = dogs_facts_api.get_facts(page, page_size, sorting)
    return schemas.GetFactsResponse(total=total,
                                    data=data)


@app.get("/api/v1/facts/{fact_id}",
         response_model=schemas.FactsResponse, status_code=200)
def get_fact_by_id(fact_id: str, auth: str = Header()):
    try:
        return dogs_facts_api.get_fact_by_id(fact_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"Fact {fact_id} is not found")


@app.delete('/api/v1/facts/{fact_id}',
            status_code=204)
def delete_fact_by_id(fact_id: str, auth: str = Header()):
    dogs_facts_api.delete_fact_by_id(fact_id)


@app.put('/api/v1/facts/{fact_id}',
         response_model=schemas.FactsResponse, status_code=201)
def change_fact_by_id(fact_id: str, fact_text: str = None,
                      interest: int = None, likes: int = None,
                      auth: str = Header()):
    try:
        return dogs_facts_api.change_fact_by_id(fact_id, fact_text, interest, likes)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"Fact {fact_id} is not found")


@app.post('/api/v1/facts/{fact_id}/like',
          response_model=schemas.FactsResponse, status_code=201)
def add_like_by_id(fact_id: str, auth: str = Header()):
    try:
        return dogs_facts_api.add_like_by_id(fact_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"Fact {fact_id} is not found")


@app.post('/api/v1/facts/import',
          response_model=schemas.ImportFactsResponse, status_code=201)
def import_facts_from_dogapi(amount: int, auth: str = Header()):
    dogs_facts_api.import_facts_from_dogapi(amount)
    return schemas.ImportFactsResponse(amount=amount)
