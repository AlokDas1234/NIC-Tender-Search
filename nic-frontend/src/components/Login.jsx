import React, { useState } from "react";
import API from "./api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async (e) => {
    e.preventDefault();

    try {
      const res = await API.post("login-page/", {
        username,
        password,
      });

      localStorage.setItem("token", res.data.token);
      localStorage.setItem("username", res.data.username);
      alert("✅ Login successful");
      window.location.reload();
    } catch (err) {
      alert("❌ Invalid credentials");
    }
  };

  return (
    <form onSubmit={login}>
      <h2>Login</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
