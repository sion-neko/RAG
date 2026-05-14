import { useState } from "react";

const API = "";

export default function App() {
  const [urlInput, setUrlInput] = useState("");
  const [indexedUrls, setIndexedUrls] = useState([]);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleIndex() {
    const urls = urlInput.split("\n").map((u) => u.trim()).filter(Boolean);
    if (!urls.length) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/index`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urls }),
      });
      if (!res.ok) {
        const err = await res.json();
        alert(`エラー: ${err.detail}`);
        return;
      }
      const data = await res.json();
      setIndexedUrls((prev) => [...new Set([...prev, ...data.indexed])]);
      setUrlInput("");
    } finally {
      setLoading(false);
    }
  }

  async function handleClear() {
    if (!confirm("インデックスを全削除しますか？")) return;
    await fetch(`${API}/index`, { method: "DELETE" });
    setIndexedUrls([]);
    setMessages([]);
  }

  async function handleQuery() {
    if (!question.trim()) return;
    const history = messages.map((m) => ({ role: m.role, content: m.content }));
    const userMsg = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await fetch(`${API}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg.content, history }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer, sources: data.sources },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleQuery();
    }
  }

  return (
    <div className="container">
      <h1>RAG App</h1>

      <section className="url-section">
        <h2>URLを登録</h2>
        <textarea
          value={urlInput}
          onChange={(e) => setUrlInput(e.target.value)}
          placeholder={"https://example.com\nhttps://example2.com"}
          rows={3}
        />
        <div className="url-actions">
          <button onClick={handleIndex} disabled={loading}>
            インデックス登録
          </button>
          <button onClick={handleClear} className="danger" disabled={loading}>
            インデックス削除
          </button>
        </div>
        {indexedUrls.length > 0 && (
          <ul className="url-list">
            {indexedUrls.map((u) => (
              <li key={u}>{u}</li>
            ))}
          </ul>
        )}
      </section>

      <section className="chat-section">
        <h2>質問する</h2>
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              <p>{m.content}</p>
              {m.sources?.length > 0 && (
                <div className="sources">
                  {m.sources.map((s) => (
                    <a key={s} href={s} target="_blank" rel="noreferrer">
                      {s}
                    </a>
                  ))}
                </div>
              )}
            </div>
          ))}
          {loading && <div className="message assistant"><p>回答中...</p></div>}
        </div>
        <div className="input-row">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="質問を入力（Enterで送信）"
            rows={2}
            disabled={loading}
          />
          <button onClick={handleQuery} disabled={loading || !question.trim()}>
            送信
          </button>
        </div>
      </section>
    </div>
  );
}
