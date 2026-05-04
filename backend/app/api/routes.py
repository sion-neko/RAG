from fastapi import APIRouter
from pydantic import BaseModel

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
    raise NotImplementedError


@router.post("/query", response_model=QueryResponse)
async def query(body: QueryRequest):
    raise NotImplementedError


@router.delete("/index")
async def clear_index():
    raise NotImplementedError
