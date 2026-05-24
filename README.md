# RAG App

URLを貼るだけで任意のWebページをRAG化して質問できる汎用RAGアプリ。

## 技術構成

| 項目 | 技術 |
|---|---|
| バックエンド | FastAPI (Python 3.11) |
| ベクトルDB | Chroma |
| 埋め込みモデル | `intfloat/multilingual-e5-small`（ローカル・日本語対応） |
| LLM | OpenAI互換API（Ollama等） |
| フロントエンド | React / Vite |
| コンテナ | Docker Compose |

## 起動方法

### 1. 環境変数の設定

```bash
cp .env.example .env
```

`.env` を編集してLLMの接続先を設定する。

```env
LLM_BASE_URL=http://host.docker.internal:11434/v1   # OllamaをホストOSで動かす場合
LLM_MODEL=llama3
LLM_API_KEY=ollama
```

### 2. 起動

```bash
docker compose up --build
```

初回はイメージビルド・モデルダウンロードがあるため数分かかる。

### 3. アクセス

| サービス | URL |
|---|---|
| フロントエンド | http://localhost:5173 |
| バックエンド API | http://localhost:8000 |
| API ドキュメント | http://localhost:8000/docs |

## API

### `POST /index` — URLをインデックス化

```json
{
  "urls": ["https://example.com/page1", "https://example.com/page2"]
}
```

### `POST /query` — 質問して回答を得る

```json
{
  "question": "このページの要点は？",
  "history": []
}
```

レスポンス:

```json
{
  "answer": "...",
  "sources": ["https://example.com/page1"]
}
```

### `DELETE /index` — インデックスを全削除

---

## バージョン履歴

### v1.0 — Webページ対応（現在）

- 複数URLを登録してソース横断検索
- Recursive Splitでチャンク分割（サイズ600〜800字、オーバーラップ150字）
- 会話履歴対応
- エンドポイント・モデル名を `.env` で切り替え可能

### v2.0 — PDF対応（予定）
