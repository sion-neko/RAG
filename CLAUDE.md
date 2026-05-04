# RAGアプリ開発

### コンセプト
「URLを貼るだけで任意のWebページをRAG化して質問できる」汎用RAGアプリ。

### 技術構成（確定）

| 項目 | 技術 |
|---|---|
| バックエンド | FastAPI（Python） |
| ベクトルDB | Chroma |
| 埋め込みモデル | `intfloat/multilingual-e5-small`（ローカル動作・日本語対応） |
| LLM | OpenAI互換API |
| データ取得 | URL入力 → スクレイピング → インデックス化 |
| インデックス更新 | 手動（ボタン一つで再インデックス） |
| コンテナ | Docker |
| UI | v0で生成 → React/Vite |

### 開発フェーズ
- **フェーズ1**：WebページURL入力対応でRAGとして動く状態を完成させる
- **フェーズ2**：PDF対応を追加

### RAGパラメータ
- チャンク戦略: Recursive Split（`\n\n` → `\n` → `. ` の順で優先分割）
- チャンクサイズ: 600〜800文字、オーバーラップ: 150文字
- top-k: 3（後で調整）

### 機能仕様
- 複数URL対応（複数登録してソース横断検索）
- 会話履歴: 保持する想定。まず最小限実装してから追加
- APIキー管理: `.env` で渡す

### LLM
- Ollama（ローカル）を使う予定。エンドポイント・モデル名は `.env` で切り替えられる設計にする

### 実装しないもの（意図的に除外）
- ファイル変更の自動検知・差分更新

---

## 現在の進捗

### 完了済み
- プロジェクト骨格（ディレクトリ構成・Dockerfile・docker-compose.yml）
- `backend/app/main.py`：FastAPI + CORS設定
- `backend/app/config.py`：`.env` 読み込み（pydantic-settings）
- `backend/app/api/routes.py`：3エンドポイント定義済み（未実装）
  - `POST /index`：URL群をインデックス化
  - `POST /query`：質問 → 回答
  - `DELETE /index`：インデックス削除
- `backend/app/services/scraper.py`：**実装済み**
  - httpxで非同期HTTP取得、BeautifulSoupでテキスト抽出
  - script/style/nav/header/footer/aside タグを除去してクリーンなテキストを返す
  - 単体実行可能：`docker-compose run --rm backend python -m app.services.scraper`

### 次にやること（順番通り）
1. `backend/app/services/indexer.py`：テキスト → Chroma保存
   - Recursive Splitでチャンク分割（サイズ600〜800、オーバーラップ150）
   - 埋め込みモデル: `intfloat/multilingual-e5-small`
   - URLをメタデータとして保存（後でsourcesとして返すため）
2. `backend/app/services/rag.py`：検索 → LLM呼び出し → 回答生成
3. `backend/app/api/routes.py`：各エンドポイントの実装を繋ぎ込む
4. フロントエンド（v0で生成 → React/Vite）


## 補足メモ
- READMEはバージョン分け（v1.0: Web対応、v2.0: PDF対応）で開発の積み重ねを可視化する