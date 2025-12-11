---

# 🚀 PromptSmith — Secure Natural Language → SQL System

![License](https://img.shields.io/badge/License-MIT-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-336791?logo=postgresql)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5-4285F4?logo=google)

PromptSmith is a **secure full-stack AI system** that converts natural language into SQL, rewrites SQL, executes queries safely, manages encrypted chat history, and includes a complete user system with admin controls.

Designed as a **production-grade academic project** demonstrating secure AI integration.

---

# 🌟 Features

## 🔐 Security

* AES-256 encryption (email, bio, chat messages)
* HMAC SHA-256 response signing
* SQL injection & safety filters
* Rate limiting via SlowAPI
* JWT authentication
* Password hashing with bcrypt
* Role-based access (admin/user)
* Local HTTPS support

---

## 🤖 NL → SQL Engine (Requires Login)

* Converts natural language into SQL using Gemini Flash 2.5
* Validates SQL for safety
* Rewrites + optimizes SQL
* Executes SQL against PostgreSQL
* Stores encrypted chat history
* Sidebar with chats, message selection, delete menu (⋮)

---

## 🛠 SQL Rewrite Engine (Public)

* Anyone can paste SQL
* Returns formatted, optimized SQL
* Response includes HMAC signature
* Rate-limited to protect API quota

---

## 👥 User Features

* Signup with emoji avatar
* Login with JWT
* Update profile (name, bio, password, image)
* AES-encrypted email + bio
* Strong password update logic

---

## 💬 Chat System

* Create/delete chats
* Encrypted user + AI messages
* Click message → autofill NL editor
* Clean UI with chat list + three-dot options

---

## 🛡 Admin Dashboard

Admins can:

* View all users
* View chats of any user
* Delete chats
* Disable users (instead of delete)
* View system analytics:

  * Total users
  * Active users
  * Total chats
  * Rewrite-SQL request count
  * NL→SQL request count

---

# 🧱 Project Structure

```
prompt_smith/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── chat_routes.py
│   │   ├── admin_routes.py
│   │   └── rewrite_routes.py
│   ├── llm/
│   │   ├── sql_gen.py
│   │   ├── sql_rewrite.py
│   │   └── safety.py
│   ├── utils/
│   │   ├── encryption.py
│   │   ├── hmac_sign.py
│   │   ├── jwt_utils.py
│   │   ├── rate_limiter.py
│   │   └── db.py
│   ├── cert.pem
│   └── key.pem
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── api/axiosAuth.js
    │   ├── App.jsx
    │   └── main.jsx
    ├── styles/
    └── vite.config.js (HTTPS enabled)
```

---

# ⚙️ Tech Stack

### Frontend

* React (Vite)
* Axios
* React Router
* Prism syntax highlighting
* Custom CSS

### Backend

* FastAPI
* PostgreSQL
* Google Gemini 2.5 Flash
* bcrypt
* Fernet AES-256
* SlowAPI rate limiting
* Uvicorn HTTPS

---

# 🔐 Security Architecture

### AES-256 Encryption

Encrypted at rest:

* Email
* Bio
* Chat messages (user + AI)

### HMAC-Signed Responses

Every LLM endpoint returns:

```json
{
  "data": {...},
  "signature": "hex-hmac"
}
```

Frontend verifies before using response.

### Rate Limiting

| Endpoint       | Limit         |
| -------------- | ------------- |
| `/rewrite-sql` | 5 per minute  |
| `/nl-to-sql`   | 10 per minute |

### Authentication

* JWT (Bearer token)
* Auto token refresh logic via Axios interceptor
* Secure cookie alternative supported

---

# 🚀 Running the Project

## 1️⃣ Backend

```sh
cd backend
pip install -r requirements.txt

uvicorn main:app --reload \
  --ssl-keyfile="key.pem" \
  --ssl-certfile="cert.pem"
```

Accessible at:

```
https://localhost:8000
```

---

## 2️⃣ Frontend

```sh
cd frontend
npm install
npm run dev
```

Runs at:

```
https://localhost:5173
```

---

# 📊 Admin Analytics Example

Dashboard displays:

* 👥 Total users
* 🟢 Active users
* 💬 Total chats
* 🤖 NL→SQL requests
* 🛠 Rewrite requests

---

# 🧪 Testing Features

### ✔ NL→SQL Query

Example:

> "Show me last 30 days revenue by customer in descending order."

### ✔ SQL Rewrite

Paste unformatted SQL → clean formatted SQL returned.

### ✔ HMAC

Modify backend response → frontend rejects.

### ✔ Encryption

Check DB — email/bio/messages unreadable (AES encoded).

---

# 🎓 Why This Project Is Strong for Academic Submission

* Full-stack implementation
* Strong security emphasis
* Real encryption & HMAC
* Local HTTPS
* SQL injection protection
* LLM integration (Gemini 2.5)
* Admin dashboard
* Clean UI + chat system

A complete production-style secure system — excellent for evaluation.

---

# 📝 License

MIT License.

---
