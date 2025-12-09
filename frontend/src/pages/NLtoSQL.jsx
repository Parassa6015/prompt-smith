import { useState, useEffect } from "react";
import api from "../api/axiosAuth";
import "../styles/nltosql.css";

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

  const [generatedSql, setGeneratedSql] = useState("");
  const [rewrittenSql, setRewrittenSql] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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

      if (res.data.error) {
        setError(res.data.error);
        setGeneratedSql("");
        setRewrittenSql("");
        setResult(null);
        setLoading(false);
        return;
      }

      setGeneratedSql(res.data.generated_sql || "");
      setRewrittenSql(res.data.final_sql || "");
      setResult(res.data.result || null);

      // If backend created a new chat, switch to it
      if (res.data.chat_id && res.data.chat_id !== selectedChat) {
        setSelectedChat(res.data.chat_id);
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
          {generatedSql && (
            <Section title="Generated SQL">
              <div className="nlts-sql-block">
                <SyntaxHighlighter language="sql" style={vscDarkPlus}>
                  {generatedSql}
                </SyntaxHighlighter>
              </div>
            </Section>
          )}

          {rewrittenSql && (
            <Section title="Rewritten SQL">
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
