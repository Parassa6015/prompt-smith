import { useState } from "react";
import api from "../api/axiosAuth";
import UserMenu from "../components/UserMenu";
import "../styles/loginsignup.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");
    try {
      const res = await api.post("/login", {
        email,
        password,
      });
      console.log("Login success", res.data);
      localStorage.setItem("token", res.data.token);
      window.location.href = "/";
    } catch (err) {
      console.error("Login error:", err);
      setError("Login failed. Check your email and password.");
    }
  };

  return (
    <div className="auth-root">
      <UserMenu />

      <div className="auth-card">
        <h1 className="auth-title">Login</h1>
        <p className="auth-subtitle">Welcome back. Sign in to your account.</p>

        <div className="auth-form">
          <div>
            <div className="auth-label">Email</div>
            <input
              type="email"
              className="auth-input"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <div className="auth-label">Password</div>
            <input
              type="password"
              className="auth-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="auth-btn" onClick={handleLogin}>
            Login
          </button>

          {error && <div className="auth-error">{error}</div>}
        </div>

        <div className="auth-footer">
          New here? <a href="/signup">Create an account</a>
        </div>
      </div>
    </div>
  );
}
