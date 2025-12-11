import { useState } from "react";
import "../styles/rewrite.css";
import UserMenu from "../components/UserMenu";
import api from "../api/axiosAuth";
import CryptoJS from "crypto-js";

export default function RewriteSql() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const HMAC_SECRET = "super-secret-hmac-key";
  
  function sortObjectKeys(obj) {
    if (obj === null || obj === undefined) {
      return obj;
    }
    
    // Handle dates, convert to ISO string like Python's default=str
    if (obj instanceof Date) {
      return obj.toISOString();
    }
    
    if (typeof obj !== 'object') {
      return obj;
    }
    
    if (Array.isArray(obj)) {
      return obj.map(sortObjectKeys);
    }
    
    const sorted = {};
    Object.keys(obj).sort().forEach(key => {
      sorted[key] = sortObjectKeys(obj[key]);
    });
    return sorted;
  }
  
  function verifySignature(data, signature) {
  const HMAC_SECRET = "super-secret-hmac-key";

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
  
  // Use separators to match Python's compact format (no spaces)
  const jsonString = JSON.stringify(sortedData, null, 0);
  
  console.log("JSON string:", jsonString);
  
  const computed = CryptoJS.HmacSHA256(jsonString, HMAC_SECRET).toString();
  
  console.log("Match:", computed === signature);
  
  return computed === signature;
}
  
  const handleRewrite = async () => {
    if (loading) return;
    setLoading(true);

    setError("");
    setOutput("");

    if (!input.trim()) {
      setError("Please paste some SQL first.");
      setLoading(false);
      return;
    }

    try {
      const res = await api.post("/rewrite-sql", {
        query: input
      });
      
      console.log("EXACT received data:", JSON.stringify(res.data.data));
      console.log("EXACT received signature:", res.data.signature);
      
      // For now, let's skip verification to see if the data is correct
      if (!verifySignature(res.data.data, res.data.signature)) {
        throw new Error("Response Integrity Check Failed");
      }

      // Temporarily disable verification to test
      const rewrittenData = res.data.data.rewritten_sql;
      
      // Check if it's a string or object
      if (typeof rewrittenData === 'string') {
        setOutput(rewrittenData);
      } else if (typeof rewrittenData === 'object') {
        // If it's an object, try to extract the SQL or stringify it
        setOutput(JSON.stringify(rewrittenData, null, 2));
      }
      
    } catch (e) {
      console.error("Rewrite error:", e);
      setError("Something went wrong while rewriting your SQL.");
    }

    setLoading(false);
  };

  return (
    <div className="rewrite-page">
      <UserMenu />

      <div className="rewrite-container">
        <h1 className="rewrite-title">SQL Formatter &amp; Optimizer</h1>
        <p className="rewrite-subtitle">
          Paste any query and get back a clean, readable version in seconds.
        </p>

        <div className="rewrite-card">
          <div className="rewrite-label">Your SQL</div>

          <textarea
            className="rewrite-textarea"
            placeholder="Paste your SQL here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />

          <button
            className="rewrite-btn"
            onClick={handleRewrite}
            disabled={loading}
          >
            {loading ? "Rewriting..." : "Rewrite SQL"}
          </button>

          {error && <div className="rewrite-error">{error}</div>}
        </div>

        {output && (
          <>
            <div className="rewrite-section-title rewrite-label">
              Reformatted SQL
            </div>

            <pre className="rewrite-output">{output}</pre>
          </>
        )}
      </div>
    </div>
  );
}