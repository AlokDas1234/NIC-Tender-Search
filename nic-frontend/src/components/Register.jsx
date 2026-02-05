// import React, { useState } from "react";
// import API from "./api";

// function Register() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [loading, setLoading] = useState(false);

//   const register = async (e) => {
//     e.preventDefault();

//     if (!username || !password) {
//       alert("Username and password are required");
//       return;
//     }

//     try {
//       setLoading(true);

//       const res = await API.post("register-page/", {
//         username,
//         password,
//       });

//       alert("✅ Registration successful. Please login.");
//       setUsername("");
//       setPassword("");

//       // optional: redirect to login
//       // window.location.href = "/login";

//     } catch (err) {
//       if (err.response?.data?.error) {
//         alert(`❌ ${err.response.data.error}`);
//       } else {
//         alert("❌ Registration failed");
//       }
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <form onSubmit={register}>
//       <h2>Register</h2>

//       <input
//         placeholder="Username"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//       />

//       <input
//         type="password"
//         placeholder="Password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//       />

//       <button type="submit" disabled={loading}>
//         {loading ? "Registering..." : "Register"}
//       </button>
//     </form>
//   );
// }

// export default Register;


import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import API from "./api";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const register = async (e) => {
    e.preventDefault();
    await API.post("register-page/", { username, password });
    alert("Registered successfully");
  };

  return (
    <form onSubmit={register}>
      <h2>Register</h2>

      <input value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />

      <button type="submit">Register</button>

      <p>
        Already have an account? <NavLink to="/login">Login</NavLink>
      </p>
    </form>
  );
}

export default Register;

