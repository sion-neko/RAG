from openai import AsyncOpenAI

from app.config import settings
from app.services.indexer import indexer

TOP_K = 3

_client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)

_SYSTEM = (
    "You are a helpful assistant. Answer the user's question using only the provided context. "
    "If the context is insufficient, say so honestly. "
    "Always reply in the same language as the user's question."
)


async def answer(question: str, history: list[dict]) -> tuple[str, list[str]]:
    """回答テキストと参照URLリストを返す。"""
    query_vec = indexer.model.encode(["query: " + question]).tolist()[0]

    results = indexer.collection.query(
        query_embeddings=[query_vec],
        n_results=TOP_K,
        include=["documents", "metadatas"],
    )

    docs: list[str] = results["documents"][0]
    metas: list[dict] = results["metadatas"][0]
    sources = list(dict.fromkeys(m["url"] for m in metas))

    context = "\n\n---\n\n".join(docs)

    messages = [
        {"role": "system", "content": _SYSTEM},
        *history,
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]

    resp = await _client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
    )

    return resp.choices[0].message.content, sources
