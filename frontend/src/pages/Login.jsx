import { useState } from "react";
import api from "../api/axiosAuth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await api.post("/login", {
        email: email,
        password: password
      });

      console.log("Login success", res.data);

      localStorage.setItem("token", res.data.token);

      window.location.href = "/";
    } catch (err) {
      console.error("Login error:", err);
    }
  };

  return (
    <div>
      <h1>Login</h1>

      <input
        type="text"
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
