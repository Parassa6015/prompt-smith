import { useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api/axiosAuth";
import UserMenu from "../components/UserMenu";
import "../styles/loginsignup.css";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/signup", {
        name,
        email,
        password,
      });
      console.log(res.data);
      alert("Signup successful! Redirecting to login...");
      navigate("/login");
    } catch (err) {
      console.error(err);
      setError("Signup failed. Email may already exist.");
    }
  };

  return (
    <div className="auth-root">
      <UserMenu />

      <div className="auth-card">
        <h1 className="auth-title">Create Account</h1>
        <p className="auth-subtitle">
          Start using PromptSmith in just a few seconds.
        </p>

        <form className="auth-form" onSubmit={handleSignup}>
          <div>
            <div className="auth-label">Full name</div>
            <input
              type="text"
              className="auth-input"
              placeholder="Ada Lovelace"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

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
              placeholder="At least 8 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="auth-btn" type="submit">
            Sign up
          </button>

          {error && <div className="auth-error">{error}</div>}
        </form>

        <div className="auth-footer">
          Already have an account? <a href="/login">Login</a>
        </div>
      </div>
    </div>
  );
}
