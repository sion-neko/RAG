import uuid

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "chroma"
COLLECTION_NAME = "documents"
CHUNK_SIZE = 700
CHUNK_OVERLAP = 150
MODEL_NAME = "intfloat/multilingual-e5-small"


class Indexer:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self._client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self._client.get_or_create_collection(COLLECTION_NAME)

    @staticmethod
    def _split(text: str) -> list[str]:
        def to_segments(text: str, seps: list[str]) -> list[str]:
            """テキストを CHUNK_SIZE 以下のセグメントに再帰分割する"""
            sep = next((s for s in seps if s in text), None)
            if sep is None:
                return [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP)]

            remaining = seps[seps.index(sep) + 1:]
            segs: list[str] = []
            for seg in text.split(sep):
                if len(seg) > CHUNK_SIZE and remaining:
                    segs.extend(to_segments(seg, remaining))
                else:
                    segs.append(seg)
            return segs

        sep = next((s for s in ["\n\n", "\n", ". ", " "] if s in text), " ")
        segs = to_segments(text, ["\n\n", "\n", ". ", " "])

        chunks: list[str] = []
        buf: list[str] = []
        for seg in segs:
            if len(sep.join(buf + [seg])) <= CHUNK_SIZE:
                buf.append(seg)
                continue
            chunk = sep.join(buf)
            if chunk:
                chunks.append(chunk)
            buf = [chunk[-CHUNK_OVERLAP:]] if chunk else []
            buf.append(seg)

        if buf:
            chunks.append(sep.join(buf))

        return chunks

    def index(self, url: str, text: str) -> int:
        chunks = self._split(text)
        if not chunks:
            return 0
        embeddings = self.model.encode(["passage: " + c for c in chunks]).tolist()
        self.collection.add(
            ids=[str(uuid.uuid4()) for _ in chunks],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"url": url} for _ in chunks],
        )
        return len(chunks)

    def clear(self) -> None:
        self._client.delete_collection(COLLECTION_NAME)
        self.collection = self._client.create_collection(COLLECTION_NAME)


indexer = Indexer()
