import React from "react";

function CodeBlock({ title, code }) {
  if (!code) return null;

  return (
    <div style={{
      background: "#1e1e1e",
      padding: "15px",
      borderRadius: "8px",
      color: "white",
      marginBottom: "15px",
      fontFamily: "monospace",
      whiteSpace: "pre-wrap"
    }}>
      <div style={{ marginBottom: "6px", fontWeight: 600 }}>
        {title} 
        <button 
          onClick={() => navigator.clipboard.writeText(code)}
          style={{ marginLeft: "10px", cursor: "pointer" }}
        >
          📋
        </button>
      </div>
      <code>{code}</code>
    </div>
  );
}

export default function ChatMessageViewer({ messages }) {
  if (!messages || messages.length === 0)
    return <div style={{ padding: "20px" }}>No messages yet.</div>;

  return (
    <div style={{ padding: "20px", flex: 1, overflowY: "auto" }}>
      {messages.map(msg => (
        <div key={msg.id} style={{ marginBottom: "30px" }}>
          <div style={{ fontWeight: 600, marginBottom: "6px" }}>
            🧑‍💻 User:
          </div>
          <div style={{ padding: "10px", background: "#f8f8f8", borderRadius: "8px" }}>
            {msg.user_message}
          </div>

          <CodeBlock title="Generated SQL" code={msg.raw_sql} />
          <CodeBlock title="Rewritten SQL" code={msg.final_sql} />

          <div style={{ fontWeight: 600, marginTop: "10px" }}>🤖 AI Result:</div>
          <pre style={{
            background: "#fafafa",
            padding: "10px",
            borderRadius: "8px",
            whiteSpace: "pre-wrap",
            overflowX: "auto"
          }}>
            {msg.ai_response}
          </pre>
        </div>
      ))}
    </div>
  );
}
