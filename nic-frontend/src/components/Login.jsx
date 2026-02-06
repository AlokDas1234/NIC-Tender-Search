import React, { useState } from "react";
// import API from "./api";
// import Register from "./Register";
// import { Routes, Route, NavLink } from "react-router-dom";
// function Login() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   const login = async (e) => {
//     e.preventDefault();

//     try {
//       const res = await API.post("login-page/", {
//         username,
//         password,
//       });

//       localStorage.setItem("token", res.data.token);
//       localStorage.setItem("username", res.data.username);
//       alert("✅ Login successful");
//       window.location.reload();
//     } catch (err) {
//       alert("❌ Invalid credentials");
//     }
//   };

//   return (
   

    
//     <form onSubmit={login}>
//       <h2>Login</h2>

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
//       <button type="submit">Login</button>
// <p><NavLink to="/register">Register</NavLink>

//     </p>
    
//     </form> 

//     //  <Routes>
//     //       <Route path="/register" element={<Register />} />
//     // </Routes>  
    
          
//   );
// }

// export default Login;import React, { useState } from "react";

import { NavLink } from "react-router-dom";
import API from "./api";
import "./auth.css";
function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("login-page/", { username, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("username", res.data.username);
      window.location.reload();
    } catch {
      alert("Invalid credentials");
    }
  };

  return (
    <form  className="auth-form" onSubmit={login}>
      <h2>Login</h2>
        <div className="form-group">
      <label htmlFor="username">User Name</label>
      <input id="username" name="username" value={username} onChange={e => setUsername(e.target.value)} />
      </div>

        <div className="form-group">
       <label  htmlFor="password">Password</label>
      <input  id="password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      </div>

      <button type="submit">Login</button>

      <p>
        New user? <NavLink to="/register">Register</NavLink>
      </p>

    </form>
  );
}

export default Login;
