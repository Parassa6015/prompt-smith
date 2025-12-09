import { useEffect, useState } from "react";
import api from "../api/axiosAuth";
import { useNavigate } from "react-router-dom";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [bio, setBio] = useState("");
  const [image, setImage] = useState("");
  const navigate = useNavigate();

  // Load profile on page load
  useEffect(() => {
    api.get("/profile")
      .then(res => {
        setProfile(res.data);
        setName(res.data.name);
      })
      .catch(() => {
        navigate("/login"); // if token invalid → send back to login
      });
  }, []);

  const handleUpdate = async () => {
    try {
      const body = {};
      if (name) body.name = name;
      if (password) body.password = password;

      const res = await api.post("/profile/update", body);
      setMessage("Profile updated successfully");
      setPassword(""); // clear password after update
      console.log(res.data);
    } catch (err) {
      setMessage("Update failed",err);
    }
  };

  if (!profile) return <div>Loading...</div>;

  return (
    <div className="profile-container">
      <h1>Your Profile</h1>

       <div className="avatar">
        <span style={{ fontSize: "60px" }}>
            {profile.avatar_emoji || "🙂"}
        </span>
      </div>

      <div className="profile-box">
        <p><strong>Email:</strong> {profile.email}</p>
        <p><strong>Role:</strong> {profile.role}</p>

        <label>Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <label>New Password (optional)</label>
        <input
          type="password"
          placeholder="Enter new password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <label>Bio</label>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            placeholder="Write something about yourself"
        />

        <label>Profile Image URL</label>
          <input
            type="text"
            value={image}
            onChange={(e) => setImage(e.target.value)}
            placeholder="Paste image link"
        />


        <button onClick={handleUpdate}>Update Profile</button>

        {message && <p className="status-msg">{message}</p>}
      </div>
    </div>
  );
}
