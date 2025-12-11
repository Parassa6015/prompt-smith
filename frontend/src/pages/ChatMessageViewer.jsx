import React from "react";

function CodeBlock({ title, code }) {
  if (!code) return null;
  return (
    <div style={{ marginTop: 8 }}>
      <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 4 }}>
        {title}
      </div>
      <pre
        style={{
          background: "#111827",
          color: "white",
          padding: 10,
          borderRadius: 8,
          fontFamily: "monospace",
          whiteSpace: "pre-wrap",
        }}
      >
        {code}
      </pre>
    </div>
  );
}

export default function ChatMessageViewer({ messages }) {
  if (!messages || messages.length === 0) {
    return <div style={{ fontSize: 13, color: "#6b7280" }}>No messages yet.</div>;
  }

  return (
    <div
      style={{
        maxHeight: 320,
        overflowY: "auto",
        paddingRight: 4,
      }}
    >
      {messages.map((msg) => (
        <div
          key={msg.id}
          style={{
            marginBottom: 20,
            paddingBottom: 16,
            borderBottom: "1px solid #e5e7eb",
          }}
        >
          <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 4 }}>You</div>
          <div
            style={{
              padding: 10,
              borderRadius: 8,
              background: "#f3f4f6",
              marginBottom: 8,
            }}
          >
            {msg.user_message}
          </div>

          <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 4 }}>
            Model
          </div>
          <div
            style={{
              padding: 10,
              borderRadius: 8,
              background: "#f9fafb",
              border: "1px solid #e5e7eb",
            }}
          >
            {msg.ai_response}
          </div>

          <CodeBlock title="Draft SQL" code={msg.raw_sql} />
          <CodeBlock title="Final SQL" code={msg.final_sql} />
        </div>
      ))}
    </div>
  );
}
