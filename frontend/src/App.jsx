import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import RewriteSQL from "./pages/RewriteSql";
import NLToSQL from "./pages/NLtoSQL";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Profile from "./pages/Profile";
import AdminDashboard from "./pages/AdminDashboard";
// Protected wrapper
function ProtectedRoute({ children, requireAdmin = false }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role"); // set role after login

  if (!token) return <Navigate to="/login" />;
  if (requireAdmin && role !== "admin") return <Navigate to="/" />;

  return children;
}

export default function App() {
  return (
    <Routes>
      
      {/* PUBLIC ROUTES */}
      <Route path="/" element={<Home />} />
      <Route path="/rewrite" element={<RewriteSQL />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* PROTECTED ROUTES */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route path="/dashboard" element={ <ProtectedRoute> <NLToSQL /> </ProtectedRoute>} />

      <Route path="/profile" element={ <ProtectedRoute> <Profile /> </ProtectedRoute>} />

    </Routes>
  );
}
