/* ---- Helper Components ---- */

export function SQLDiff({ original, rewritten }) {
  const oLines = original.split("\n");
  const rLines = rewritten.split("\n");

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>SQL Diff</h3>

      <pre
        style={{
          background: "#1e1e1e",
          color: "#ddd",
          padding: "16px",
          borderRadius: "6px",
          fontFamily: "monospace",
          lineHeight: "1.5em",
          overflowX: "auto",
        }}
      >
        {oLines.map((line, i) => {
          const newLine = rLines[i] || "";

          // No change → grey
          if (line.trim() === newLine.trim()) {
            return (
              <div key={i} style={{ color: "#aaa" }}>
                {"  "}{line}
              </div>
            );
          }

          // Changed → red old line, green new line
          return (
            <div key={i}>
              <div style={{ color: "#ff6b6b" }}>
                - {line}
              </div>
              <div style={{ color: "#7bed9f" }}>
                + {newLine}
              </div>
            </div>
          );
        })}
      </pre>
    </div>
  );
}

export function Section({ title, children }) {
  return (
    <div style={{ marginBottom: "30px" }}>
      <h3
        style={{
          fontSize: "20px",
          fontWeight: "600",
          marginBottom: "10px",
          borderBottom: "2px solid #eee",
          paddingBottom: "6px",
        }}
      >
        {title}
      </h3>
      {children}
    </div>
  );
}

export function CodeBlock({ children }) {
  return (
    <pre
      style={{
        background: "#f4f4f4",
        padding: "15px",
        borderRadius: "8px",
        whiteSpace: "pre-wrap",
        fontSize: "15px",
      }}
    >
      {children}
    </pre>
  );
}

export function ResultsTable({ result }) {
  if (!result || !result.rows || result.rows.length === 0) {
    return <p>No rows returned.</p>;
  }

  return (
    <div>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: "15px",
        }}
      >
        <thead>
          <tr>
            {result.columns.map((col) => (
              <th
                key={col}
                style={{
                  borderBottom: "2px solid #ccc",
                  padding: "8px",
                  textAlign: "left",
                }}
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {result.rows.map((row, idx) => (
            <tr key={idx}>
              {result.columns.map((col) => (
                <td
                  key={col}
                  style={{
                    padding: "8px",
                    borderBottom: "1px solid #eee",
                  }}
                >
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {/* Execution time */}
      {result.time_ms !== undefined && (
        <p
          style={{
            marginTop: "10px",
            fontSize: "14px",
            color: "#666",
          }}
        >
          Query executed in <strong>{result.time_ms} ms</strong>
        </p>
      )}
    </div>
  );
}

export function SqlBlock({ title, sql }) {
  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <h3 style={{ fontWeight: "600", marginBottom: "6px" }}>{title}</h3>
      <pre
        style={{
          background: "#1e1e1e",
          color: "#dcdcdc",
          padding: "12px",
          borderRadius: "6px",
          overflowX: "auto",
          lineHeight: "1.4",
          fontSize: "14px",
        }}
      >
        <code>{sql}</code>
      </pre>
    </div>
  );
}