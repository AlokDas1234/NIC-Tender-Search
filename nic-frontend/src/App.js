// import "./App.css";
// import GetTenders from "./components/GetTenders";
// import GetReq from "./components/GetUserReq";
// import GetFields from "./components/GetClientField";
// import Login from "./components/Login";
// import Register from "./components/Register";
// import GetUserInfo from "./components/GetUsername";
// import GetSearcReq from "./components/SearchReq";
// import Dashboard from "./components/Dashboard";

// import { Routes, Route, NavLink } from "react-router-dom";

// function App() {
//   const token = localStorage.getItem("token");

// function Logout (){   
//   const confirm = window.confirm(
//       "⚠️ This will logout. Are you sure?"
//     );
//     if (!confirm) return;
//     if (confirm){
//     localStorage.removeItem("token");
//     window.location.reload();
//     };
 
//   };
  

//   if (!token) {
//     return <Login />;
//   }

//   return (
//     <div className="app-container">
//       {/* HEADER */}
//       <header className="app-header">
//         <h1>NIC Tender Dashboard</h1>
//         <div className="user-info">
//           <span>{localStorage.getItem("username")}</span>
//           <NavLink onClick={ Logout} className="logout-btn">Logout</NavLink>

       
//         </div>
//       </header>

//       {/* NAVIGATION */}
//       <nav className="app-nav">
//         <NavLink to="/requirements">Requirements</NavLink>
//         <NavLink to="/">Dashboard</NavLink>
//         <NavLink to="/search">Search Tender</NavLink>
//         <NavLink to="/tenders">Tenders</NavLink>
//       </nav>

//       {/* CONTENT */}
//       <main className="app-content">
//         <Routes>
//           <Route path="/" element={<Dashboard />} />
//           <Route path="/requirements" element={<GetReq />} />
        
//           <Route path="/tenders" element={<GetTenders />} />
//           <Route path="/search" element={<GetSearcReq />} />
 
//           <Route path="/fields" element={<GetFields />} />
//           <Route path="/user" element={<GetUserInfo />} />
//           <Route path="/logout" element={<Logout />} />
//         </Routes>
//       </main>
//     </div>
//   );
// }

// export default App;


import "./App.css";
import { Routes, Route, NavLink, Navigate } from "react-router-dom";

import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import GetTenders from "./components/GetTenders";
import GetReq from "./components/GetUserReq";
import GetFields from "./components/GetClientField";
import GetUserInfo from "./components/GetUsername";
import GetSearcReq from "./components/SearchReq";

function App() {
  const token = localStorage.getItem("token");

  const Logout = () => {
    const confirm = window.confirm("⚠️ This will logout. Are you sure?");
    if (!confirm) return;
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <Routes>
      {/* PUBLIC ROUTES */}
      <Route
        path="/login"
        element={token ? <Navigate to="/" /> : <Login />}
      />
      <Route
        path="/register"
        element={token ? <Navigate to="/" /> : <Register />}
      />

      {/* PROTECTED ROUTES */}
      <Route
        path="/*"
        element={
          token ? (
            <div className="app-container">
              <header className="app-header">
                <h1>NIC Tender Dashboard</h1>
                <div className="user-info">
                  <span>{localStorage.getItem("username")}</span>
                  <NavLink onClick={Logout} className="logout-btn">
                    Logout
                  </NavLink>
                </div>
              </header>

              <nav className="app-nav">
                <NavLink to="/">Dashboard</NavLink>
                <NavLink to="/requirements">Requirements</NavLink>
                <NavLink to="/search">Search Tender</NavLink>
                <NavLink to="/tenders">Tenders</NavLink>
              </nav>

              <main className="app-content">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/requirements" element={<GetReq />} />
                  <Route path="/tenders" element={<GetTenders />} />
                  <Route path="/search" element={<GetSearcReq />} />
                  <Route path="/fields" element={<GetFields />} />
                  <Route path="/user" element={<GetUserInfo />} />
                </Routes>
              </main>
            </div>
          ) : (
            <Navigate to="/login" />
          )
        }
      />
    </Routes>
  );
}

export default App;

