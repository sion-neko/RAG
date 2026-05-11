from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.indexer import indexer
from app.services.rag import answer
from app.services.scraper import scrape

router = APIRouter()


class IndexRequest(BaseModel):
    urls: list[str]


class QueryRequest(BaseModel):
    question: str
    history: list[dict] = []


class IndexResponse(BaseModel):
    indexed: list[str]


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/index", response_model=IndexResponse)
async def index_urls(body: IndexRequest):
    indexed = []
    for url in body.urls:
        try:
            text = await scrape(url)
            indexer.index(url, text)
            indexed.append(url)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"{url}: {e}")
    return IndexResponse(indexed=indexed)


@router.post("/query", response_model=QueryResponse)
async def query(body: QueryRequest):
    ans, sources = await answer(body.question, body.history)
    return QueryResponse(answer=ans, sources=sources)


@router.delete("/index", status_code=204)
async def clear_index():
    indexer.clear()
