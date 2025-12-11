// Home.jsx
import { useNavigate } from "react-router-dom";
import "../styles/home.css";
import UserMenu from "../components/UserMenu";

export default function Home() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  return (
    <div className="home-root">
      <UserMenu />

      <header className="home-hero">
        <span className="home-pill">⚙️ PromptSmith</span>
        <h1 className="home-title">Work with SQL in seconds</h1>
        <p className="home-subtitle">
          Format existing queries or generate new ones from natural language.
        </p>
      </header>

      <section className="home-card-container">
        <button
          className="home-card home-card-public"
          onClick={() => navigate("/rewrite")}
        >
          <span className="home-card-tag">No login</span>
          <h2>🛠 Rewrite SQL</h2>
          <p>Instantly format and optimize SQL you already have.</p>
        </button>

        <button
          className="home-card home-card-secure"
          onClick={() => (!token ? navigate("/login") : navigate("/dashboard"))}
        >
          <span className="home-card-tag home-card-tag-secure">
            Requires account
          </span>
          <h2>🤖 NL → SQL</h2>
          <p>Describe what you want and get a ready‑to‑run query.</p>
        </button>
      </section>

      <section className="home-footer-hints">
        <div>© {new Date().getFullYear()} Noice AI. All rights reserved.</div>
        <div>Privacy · Terms · Support</div>
      </section>
    </div>
  );
}
