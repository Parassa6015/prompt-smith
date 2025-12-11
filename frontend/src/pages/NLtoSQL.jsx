import { useState, useEffect } from "react";
import api from "../api/axiosAuth";
import "../styles/nltosql.css";
import UserMenu from "../components/UserMenu";
import CryptoJS from "crypto-js";
import ChatSidebar from "./ChatSidebar";

import { Section, ResultsTable } from "../components/helperComponents";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function NLtoSQL() {
  const [prompt, setPrompt] = useState("");
  const [model, setModel] = useState("gemini");
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [messages, setMessages] = useState([]);

  const [, setGeneratedSql] = useState("");
  const [rewrittenSql, setRewrittenSql] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function verifySignature(data, signature) {
    const HMAC_SECRET = "super-secret-hmac-key";

    // Deep sort function to match Python json.dumps(sort_keys=True)
    function deepSort(obj) {
      if (Array.isArray(obj)) {
        return obj.map(deepSort);
      } else if (obj && typeof obj === "object") {
        return Object.keys(obj)
          .sort()
          .reduce((acc, key) => {
            acc[key] = deepSort(obj[key]);
            return acc;
          }, {});
      }
      return obj;
    }

  const sortedData = deepSort(data);
  const jsonString = JSON.stringify(sortedData);

  const computed = CryptoJS.HmacSHA256(jsonString, HMAC_SECRET).toString();
  return computed === signature;
}

  // Load chat list
  const loadChats = async () => {
    try {
      const res = await api.get("/chats/list");
      setChats(res.data || []);
    } catch (err) {
      console.error("Failed to load chats:", err);
    }
  };

  useEffect(() => {
    loadChats();
  }, []);

  // Load messages when chat selected
  useEffect(() => {
    if (!selectedChat) return;

    api.get(`/chats/${selectedChat}/messages`)
      .then(res => setMessages(res.data || []))
      .catch(err => console.error("Failed to load messages", err));
  }, [selectedChat]);

  // Submit NL → SQL
  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
    const res = await api.post("/nl-to-sql", {
        prompt,
        model,
        chat_id: selectedChat
    });

    // ---------- HMAC SECURITY CHECK ----------
    if (!verifySignature(res.data.data, res.data.signature)) {
        setError("Response integrity check failed!");
        return;
    }
    const payload = res.data.data;
    // ------------------------------------------

    setGeneratedSql(payload.generated_sql || "");
    setRewrittenSql(payload.final_sql || "");
    setResult(payload.result || null);

    if (payload.chat_id && payload.chat_id !== selectedChat) {
        setSelectedChat(payload.chat_id);
        loadChats();
    }

} catch (err) {
    console.error(err);
    setError("Request failed");
}

    setLoading(false);
  };

  return (
    <div className="main-layout">
      
      {/* LEFT SIDEBAR */}
      <ChatSidebar
        chats={chats}
        messages={messages}
        selectedChatId={selectedChat}
        onSelectChat={setSelectedChat}
        onSelectMessage={(msg) => setPrompt(msg)}
        onChatCreated={(newId) => {
          loadChats();
          setSelectedChat(newId);
          setPrompt("");
          setGeneratedSql("");
          setRewrittenSql("");
          setResult(null);
          setMessages([]);
        }}
      />

      {/* MAIN CONTENT */}
      <div className="content-area">
        <UserMenu />
        <div className="nlts-page">
          <h1 className="nlts-title">Natural Language → SQL</h1>

          <div className="nlts-card">
            <textarea
              className="nlts-textarea"
              placeholder="Ask anything…"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />

            <div className="nlts-row">
              <select
                className="nlts-select"
                value={model}
                onChange={(e) => setModel(e.target.value)}
              >
                <option value="gemini">Gemini Flash 2.5</option>
                <option value="ollama">Ollama (sqlcoder)</option>
              </select>

              <button className="nlts-btn" disabled={loading} onClick={handleSubmit}>
                {loading ? "Generating…" : "Run"}
              </button>
            </div>

            {error && <div className="nlts-error">⚠ {error}</div>}
          </div>

          {/* RESULT BLOCKS */}
          {/* {generatedSql && (
            <Section title="Generated SQL">
              <div className="nlts-sql-block">
                <SyntaxHighlighter language="sql" style={vscDarkPlus}>
                  {generatedSql}
                </SyntaxHighlighter>
              </div>
            </Section>
          )} */}

          {rewrittenSql && (
            <Section title="Written SQL">
              <div className="nlts-sql-block">
                <SyntaxHighlighter language="sql" style={vscDarkPlus}>
                  {rewrittenSql}
                </SyntaxHighlighter>
              </div>
            </Section>
          )}

          {result && (
            <Section title="Results">
              <ResultsTable result={result} />
            </Section>
          )}
        </div>
      </div>
    </div>
  );
}
