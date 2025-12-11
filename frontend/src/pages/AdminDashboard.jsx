import { useEffect, useState } from "react";
import api from "../api/axiosAuth";
import "../styles/admin.css";
import UserMenu from "../components/UserMenu";

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userChats, setUserChats] = useState([]);
  const [chatModalOpen, setChatModalOpen] = useState(false);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const res = await api.get("/admin/users");
      setUsers(res.data);
    } catch (err) {
      console.error("Failed to load users", err);
    }
    setLoading(false);
  };

  const loadAnalytics = async () => {
    try {
      const res = await api.get("/admin/analytics");
      setAnalytics(res.data);
    } catch (err) {
      console.error("Failed to load analytics", err);
    }
  };

  const loadUserChats = async (userId) => {
    try {
      const res = await api.get(`/admin/users/${userId}/chats`);
      setUserChats(res.data);
    } catch (err) {
      console.error("Failed to load chats", err);
    }
  };

  useEffect(() => {
    loadUsers();
    loadAnalytics();
  }, []);

  const deleteUser = async (id) => {
    if (!window.confirm("Delete this user permanently?")) return;

    try {
      await api.delete(`/admin/users/${id}`);
      loadUsers();
      loadAnalytics();
    } catch (err) {
      console.error("Failed to delete user", err);
    }
  };

  const openChatModal = async (user) => {
    setSelectedUser(user);
    await loadUserChats(user.id);
    setChatModalOpen(true);
  };

  const deleteChat = async (chatId) => {
    if (!window.confirm("Delete this chat permanently?")) return;

    try {
      await api.delete(`/admin/chats/${chatId}`);
      await loadUserChats(selectedUser.id);
      loadAnalytics();
    } catch (err) {
      console.error("Failed to delete chat", err);
    }
  };

  return (
    <div className="admin-page">
      <UserMenu />

      <h1 className="admin-title">Admin Dashboard</h1>
      <p className="admin-subtitle">Manage users, chats, and system activity</p>

      {/* ====================== ANALYTICS PANEL ====================== */}
      {analytics && (
        <div className="admin-analytics">
          <div className="admin-stat">
            <span className="stat-value">{analytics.total_users}</span>
            <span className="stat-label">Total Users</span>
          </div>

          <div className="admin-stat">
            <span className="stat-value">{analytics.total_chats}</span>
            <span className="stat-label">Total Chats</span>
          </div>

          <div className="admin-stat">
            <span className="stat-value">{analytics.total_messages}</span>
            <span className="stat-label">Total Messages</span>
          </div>

          <div className="admin-stat">
            <span className="stat-value">{analytics.llm_usage}</span>
            <span className="stat-label">LLM Calls</span>
          </div>
        </div>
      )}

      {loading && <p className="admin-loading">Loading users…</p>}

      {/* ====================== USER CARDS ====================== */}
      <div className="admin-grid">
        {users.map((u) => (
          <div className="admin-user-card" key={u.id}>
            <div className="admin-user-header">
              <span className="admin-emoji">{u.avatar_emoji || "👤"}</span>
              <div>
                <div className="admin-name">{u.name}</div>
                <div className="admin-email">{u.email}</div>
                <div className="admin-role">{u.role}</div>
              </div>
            </div>

            {u.bio && <p className="admin-bio">{u.bio}</p>}

            <div className="admin-actions">
              <button
                className="admin-btn view-btn"
                onClick={() => openChatModal(u)}
              >
                View Chats
              </button>
              <button
                className="admin-btn delete-btn"
                onClick={() => deleteUser(u.id)}
              >
                Delete User
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* ====================== CHAT MODAL ====================== */}
      {chatModalOpen && (
        <div className="admin-modal-overlay" onClick={() => setChatModalOpen(false)}>
          <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
            <h2>Chats of {selectedUser?.name}</h2>

            {userChats.length === 0 && <p>No chats found.</p>}

            {userChats.map((c) => (
              <div className="admin-chat-item" key={c.id}>
                <div>
                  <strong>Chat #{c.id}</strong>
                  <div className="admin-chat-date">
                    {new Date(c.updated_at).toLocaleString()}
                  </div>
                </div>
                <button
                  className="admin-chat-delete"
                  onClick={() => deleteChat(c.id)}
                >
                  Delete
                </button>
              </div>
            ))}

            <button className="admin-close-btn" onClick={() => setChatModalOpen(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
