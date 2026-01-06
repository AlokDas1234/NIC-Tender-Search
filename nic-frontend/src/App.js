import "./App.css";
import GetTenders from "./components/GetTenders";
import GetReq from "./components/GetUserReq";
import GetFields from "./components/GetClientField";
import Login from "./components/Login";
import GetUserInfo from "./components/GetUsername";
import GetSearcReq from "./components/SearchReq";
import Dashboard from "./components/Dashboard";

import { Routes, Route, NavLink } from "react-router-dom";

function App() {
  const token = localStorage.getItem("token");

function Logout (){   
  const confirm = window.confirm(
      "⚠️ This will logout. Are you sure?"
    );
    if (!confirm) return;
    if (confirm){
    localStorage.removeItem("token");
    window.location.reload();
    };
 
  };
  

  if (!token) {
    return <Login />;
  }

  return (
    <div className="app-container">
      {/* HEADER */}
      <header className="app-header">
        <h1>NIC Tender Dashboard</h1>
        <div className="user-info">
          <span>{localStorage.getItem("username")}</span>
          <NavLink onClick={ Logout} className="logout-btn">Logout</NavLink>
        </div>
      </header>

      {/* NAVIGATION */}
      <nav className="app-nav">
        <NavLink to="/requirements">Requirements</NavLink>
        <NavLink to="/">Dashboard</NavLink>
      
        <NavLink to="/search">Search Tender</NavLink>
        <NavLink to="/tenders">Tenders</NavLink>

      </nav>

      {/* CONTENT */}
      <main className="app-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/requirements" element={<GetReq />} />
          <Route path="/tenders" element={<GetTenders />} />
          <Route path="/search" element={<GetSearcReq />} />
 
          <Route path="/fields" element={<GetFields />} />
          <Route path="/user" element={<GetUserInfo />} />
          <Route path="/logout" element={<Logout />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
