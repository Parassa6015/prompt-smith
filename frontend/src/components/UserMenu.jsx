import { useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import api from "../api/axiosAuth";
import "../styles/usermenu.css";

export default function UserMenu() {
  const [user, setUser] = useState(null);
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // Fetch user profile
  const fetchUser = async () => {
    if (!token) return;
    try {
      const res = await api.get("/profile");
      setUser(res.data);
    } catch (err) {
      console.error("Failed to fetch user:", err);
    }
  };

  // load profile only if logged in
  useEffect(() => {
    fetchUser();
  }, [token]);

  // Refresh user on window focus
  useEffect(() => {
    const handleFocus = () => fetchUser();
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, [token]);

  // close on outside click
  useEffect(() => {
    const handler = (e) => {
      if (!menuRef.current) return;
      if (!menuRef.current.contains(e.target)) setOpen(false);
    };
    if (open) document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [open]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("name");
    setUser(null);
    setOpen(false);
    navigate("/");
  };

  const initials =
    user?.name
      ?.split(" ")
      .map((p) => p[0])
      .join("")
      .toUpperCase() || "U";

  // Check if user is admin
  const isAdmin = user?.role === "admin";

  return (
    <div className="menu-container">
      {/* top nav buttons */}
      <div className="top-nav">
        <button onClick={() => navigate("/")}>Home</button>
        <button onClick={() => navigate("/rewrite")}>Rewrite</button>
        <button onClick={async() => { try { await api.post("/chats/create"); navigate("/dashboard"); } catch(e) { console.error(e); } }}>NL→SQL</button>
        
        {/* Admin Dashboard button - only visible to admins */}
        {isAdmin && (
          <button className="admin-btn" onClick={() => navigate("/admin")}>
            Admin Dashboard
          </button>
        )}
      </div>

      {/* profile avatar */}
      <div className="menu-wrapper" ref={menuRef}>
        <div
          className="avatar-circle"
          onClick={() => setOpen((v) => !v)}
          aria-haspopup="menu"
          aria-expanded={open}
        >
          {initials}
        </div>

        {/* dropdown */}
        {open && (
          <div className="profile-menu" role="menu">
            {token ? (
              <>
                <div className="menu-header">
                  <div className="menu-name">{user?.name || "Account"}</div>
                  <div className="menu-email">{user?.email}</div>
                  {isAdmin && (
                    <div style={{ 
                      fontSize: "11px", 
                      color: "#667eea", 
                      fontWeight: "600",
                      marginTop: "4px" 
                    }}>
                      ADMIN
                    </div>
                  )}
                </div>
                <button
                  className="menu-item"
                  onClick={() => {
                    navigate("/profile");
                    setOpen(false);
                    setTimeout(fetchUser, 100);
                  }}
                >
                  Profile
                </button>
                
                {/* Admin Dashboard in dropdown menu */}
                {isAdmin && (
                  <button
                    className="menu-item"
                    onClick={() => {
                      navigate("/admin");
                      setOpen(false);
                    }}
                  >
                    Admin Dashboard
                  </button>
                )}
                
                <button className="menu-item logout" onClick={handleLogout}>
                  Log out
                </button>
              </>
            ) : (
              <>
                <div className="menu-header">Welcome</div>
                <button
                  className="menu-item"
                  onClick={() => {
                    navigate("/login");
                    setOpen(false);
                  }}
                >
                  Log in
                </button>
                <button
                  className="menu-item"
                  onClick={() => {
                    navigate("/signup");
                    setOpen(false);
                  }}
                >
                  Sign up
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}