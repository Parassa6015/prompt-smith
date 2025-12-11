import "../styles/chatbar.css";
import api from "../api/axiosAuth";
import { useState } from "react";

export default function ChatSidebar({
  chats,
  messages,
  selectedChatId,
  onSelectChat,
  onSelectMessage,
  onChatCreated
}) {
  const [menuOpen, setMenuOpen] = useState(null); // chatId of open dropdown

  // Create new chat
  const handleNewChat = async () => {
    try {
      const res = await api.post("/chats/create");
      onSelectChat(res.data.chat_id);
      if (onChatCreated) onChatCreated();
    } catch (err) {
      console.error("Failed to create chat", err);
    }
  };

  // Delete chat
  const deleteChat = async (chatId) => {
    try {
      await api.delete(`/chats/${chatId}`);

      if (selectedChatId === chatId) {
        onSelectChat(null);
      }

      if (onChatCreated) onChatCreated();
      setMenuOpen(null);
    } catch (err) {
      console.error("Failed to delete chat:", err);
    }
  };

  return (
    <div className="sidebar">
      <h3 className="sidebar-title">💬 Chat History</h3>

      <button
        className="new-chat-btn"
        onClick={async () => {
          try {
            const res = await api.post("/chats/create");
            const newChatId = res.data.chat_id;

            // set active chat
            onSelectChat(newChatId);

            // notify parent (NLtoSQL)
            if (onChatCreated) onChatCreated(newChatId);

          } catch (err) {
            console.error("Failed to create chat", err);
          }
        }}
      >
        + New Chat
      </button>


      <div className="chat-list">
        {chats?.map((chat) => (
          <div
              key={chat.id}
              className={`chat-item ${selectedChatId === chat.id ? "selected" : ""}`}
            >
              <div className="chat-info" onClick={() => onSelectChat(chat.id)}>
              📄 Chat #{chat.id}
              <div className="chat-date">
                {new Date(chat.updated_at).toLocaleString()}
              </div>
            </div>

            {/* Three-dot menu */}
            <div
              className="menu-wrapper"
              onClick={(e) => e.stopPropagation()}  // prevents click bubbling
            >
              {/* Three-dot button */}
              <button
                className="menu-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  setMenuOpen(menuOpen === chat.id ? null : chat.id);
                }}
              >
                ⋮
              </button>

              {/* Dropdown menu */}
              {menuOpen === chat.id && (
                <div
                  className="dropdown-menu"
                  onClick={(e) => e.stopPropagation()} // prevents closing when clicking inside
                >
                  <button
                    className="dropdown-item delete-item"
                    onClick={() => {
                      deleteChat(chat.id);
                      setMenuOpen(null);
                    }}
                  >
                    🗑️ Delete chat
                  </button>
                </div>
            )}
          </div>

          </div>
        ))}
      </div>

      {messages && messages.length > 0 && (
        <div className="messages-section">
          {messages.map((m) => (
            <div
              key={m.id}
              className="message-item"
              onClick={() => onSelectMessage(m.user_message)}
            >
              🧑 {m.user_message}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
