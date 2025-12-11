import { useEffect, useState } from "react";
import api from "../api/axiosAuth";
import { useNavigate } from "react-router-dom";
import UserMenu from "../components/UserMenu";
import "../styles/loginsignup.css";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [name, setName] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [bio, setBio] = useState("");
  const [image, setImage] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  // Load profile on page load
  useEffect(() => {
    api
      .get("/profile")
      .then((res) => {
        setProfile(res.data);
        setName(res.data.name || "");
        setBio(res.data.bio || "");
        setImage(res.data.image || "");
      })
      .catch(() => {
        navigate("/login"); // if token invalid → send back to login
      });
  }, [navigate]);

  const handleUpdate = async () => {
  try {
    const body = {
      name,
      bio,
      image,
    };

    if (newPassword) {
      body.current_password = currentPassword;
      body.new_password = newPassword;
    }

    const res = await api.post("/profile/update", body);
    setMessage("Profile updated successfully");
    // Clear password fields
    setCurrentPassword("");
    setNewPassword("");

  } catch (err) {
    console.error(err);
    setMessage(err.response?.data?.detail || "Update failed");
  }
};


  if (!profile) {
    return (
      <div className="auth-root">
        <div className="auth-card">
          <p>Loading profile…</p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-root">
      <div className="auth-top-nav">
        <UserMenu />
      </div>

      <div className="auth-card">
        <h1 className="auth-title">Your Profile</h1>
        <p className="auth-subtitle">
          View and update your account details.
        </p>

        <div style={{ display: "flex", alignItems: "center", marginBottom: 16 }}>
          <span style={{ fontSize: 40, marginRight: 12 }}>😊</span>
          {image && (
            <img
              src={image}
              alt="Profile"
              style={{
                width: 56,
                height: 56,
                borderRadius: "999px",
                objectFit: "cover",
                border: "1px solid #e5e7eb",
              }}
            />
          )}
        </div>

        <p style={{ marginBottom: 4 }}>
          <strong>Email:</strong> {profile.email}
        </p>
        <p style={{ marginBottom: 16 }}>
          <strong>Role:</strong> {profile.role}
        </p>

        <div className="auth-form">
          <div className="auth-field">
            <label className="auth-label">Name</label>
            <input
              className="auth-input"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Current Password</label>
            <input
              className="auth-input"
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder="Enter current password"
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">New Password (optional)</label>
            <input
              className="auth-input"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter new password"
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Bio</label>
            <textarea
              className="auth-input"
              rows={3}
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="Write something about yourself"
              style={{ resize: "vertical" }}
            />
          </div>

          <div className="auth-field">
            <label className="auth-label">Profile Image URL</label>
            <input
              className="auth-input"
              type="text"
              value={image}
              onChange={(e) => setImage(e.target.value)}
              placeholder="Paste image link"
            />
          </div>

          <button type="button" className="auth-btn" onClick={handleUpdate}>
            Update Profile
          </button>

          {message && <div className="auth-error">{message}</div>}
        </div>
      </div>
    </div>
  );
}
