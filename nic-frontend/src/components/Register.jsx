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

import "./auth.css";
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
    // <form onSubmit={register}>
    //   <h2>Register</h2>
      
    //   <label for="username">User Name:</label>
    //   <input name="username" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
    //   <br></br>
    //    <label for="password">Password:</label>
    //   <input name="password" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
    //    <br></br>
    //   <button type="submit">Register</button>

    //   <p>
    //     Already have an account? <NavLink to="/login">Login</NavLink>
    //   </p>
    // </form>

    <form className="auth-form" onSubmit={register}>
  <h2>Create Account</h2>

  <div className="form-group">
    <label htmlFor="username">Username</label>
    <input
      id="username"
      name="username"
      placeholder="Enter username"
      value={username}
      onChange={(e) => setUsername(e.target.value)}
      required
    />
  </div>

  <div className="form-group">
    <label htmlFor="password">Password</label>
    <input
      id="password"
      name="password"
      type="password"
      placeholder="Enter password"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      required
    />
  </div>

  <button type="submit" className="primary-btn">
    Register
  </button>

  <p className="auth-switch">
    Already have an account ? <NavLink to="/login">Login</NavLink>
  </p>

</form>

  );
}

export default Register;

