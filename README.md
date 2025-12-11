# 🚀 PromptSmith – Secure Natural Language → SQL System

![License](https://img.shields.io/badge/License-MIT-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-336791?logo=postgresql)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5-4285F4?logo=google)

PromptSmith is a **secure, production-grade full-stack AI system** that converts natural language into SQL, rewrites and optimizes SQL queries, executes them safely, and manages encrypted chat history with a complete admin control panel.

**Key Highlights:**
- NL → SQL Generator (authenticated users only)
- SQL Rewrite/Formatter (public access)
- AES-256 encrypted user data
- HMAC-SHA256 signed responses
- JWT authentication with role-based access
- Rate limiting for API protection
- Admin dashboard with user & chat management
- Local HTTPS support

---

## 🌟 Features

### 🔐 Security Features

- **AES-256 Encryption** – User emails, bios, and all chat messages stored encrypted
- **HMAC SHA-256 Response Signing** – Protects NL→SQL & RewriteSQL endpoints from tampering
- **SQL Injection Protection** – Safety filters validate all generated SQL
- **Rate Limiting** – Prevents LLM abuse and protects system resources via SlowAPI
- **JWT Authentication** – Required for NL→SQL, chat history, profile updates, and admin access
- **Password Security** – bcrypt hashing with strong password requirements
- **HTTPS Support** – Backend runs with SSL certificates (cert.pem/key.pem)
- **Role-Based Access Control** – Separate admin/user permissions

---

### 🤖 NL → SQL Engine (Requires Login)

- Converts natural language into SQL using **Gemini Flash 2.5**
- Validates SQL for safety and injection risks
- Rewrites and optimizes generated SQL
- Executes SQL queries against PostgreSQL securely
- Stores encrypted chat history with full conversation context
- Chat sidebar with message selection and delete options (⋮)
- Click any message to autofill the NL editor

---

### 🛠 SQL Rewrite Engine (Public Access)

- Anyone can use without login
- Paste unformatted SQL → receive formatted, optimized SQL
- Format, optimize, and rewrite SQL queries
- HMAC-verified response for integrity
- Rate-limited to protect API quota

---

### 👥 User Management

- **Signup** with emoji avatar selection
- **Login** with JWT token authentication
- **Profile Management**:
  - Update name, bio, password
  - Upload profile image
  - AES-encrypted email and bio
  - Strong password validation
- View personal chat history
- Delete own chats

---

### 💬 Chat System

- Create and manage multiple chat sessions
- Encrypted storage of user prompts and AI responses
- Click any message to reuse in editor
- Delete individual chats via three-dot menu
- Clean UI with chat list and message viewer
- Rename chats (coming soon)

---

### 🛡 Admin Dashboard

Admins have complete system oversight:

**User Management:**
- View all registered users
- View any user's chat history
- Disable/enable user accounts (soft delete)
- Monitor user activity

**System Analytics:**
- 👥 Total users count
- 🟢 Active users count
- 💬 Total chats across system
- 🤖 NL→SQL request count
- 🛠 Rewrite-SQL request count
- LLM usage statistics

**Chat Management:**
- View chats of any user
- Delete any chat in the system
- Monitor system-wide chat activity

---

## 📁 Complete Project Structure

```
PROMPT_SMITH/
│
├── backend/
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── admin_routes.py          # Admin dashboard endpoints
│   │   ├── auth.py                  # Login, signup, profile routes
│   │   └── chat_routes.py           # Chat CRUD operations
│   │
│   ├── services/
│   │   ├── __pycache__/
│   │   ├── __auth_service/
│   │   │   └── __pycache__/
|   |   |   └── auth_service.py      # Authentication business logic
│   │   ├── cleaner.py               # Data cleaning utilities
│   │   ├── gemini_service.py        # Gemini LLM integration
│   │   ├── instruction_search.py    # Instruction processing
│   │   ├── llm_service.py           # LLM service orchestration
│   │   ├── nl_to_sql_service.py     # Natural Language to SQL conversion
│   │   ├── schema_service.py        # Database schema management
│   │   └── sql_validator.py         # SQL validation and safety checks
│   │
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── correctness.py           # SQL correctness validation
│   │   ├── db.py                    # PostgreSQL connection management
│   │   ├── encryption.py            # AES-256 encryption utilities
│   │   ├── hmac_sign.py             # HMAC signature generation
│   │   ├── rate_limiter.py          # Rate limiting configuration
│   │   └── sql_executor.py          # Safe SQL execution wrapper
│   │
│   ├── venv/                        # Python virtual environment
│   ├── .env                         # Environment variables (not in Git)
│   ├── cert.pem                     # SSL certificate
│   ├── key.pem                      # SSL private key
│   ├── main.py                      # FastAPI application entry point
│   └── requirement.txt              # Python dependencies
│
├── frontend/
│   ├── node_modules/                # npm packages
│   ├── public/                      # Static assets
│   │
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.js              # Auth API calls
│   │   │   └── axiosAuth.js         # Axios instance with JWT interceptor
│   │   │
│   │   ├── assets/                  # Images and static files
│   │   │
│   │   ├── components/
│   │   │   ├── helperComponents.jsx # Reusable UI components
│   │   │   └── UserMenu.jsx         # User dropdown menu
│   │   │
│   │   ├── pages/
│   │   │   ├── AdminDashboard.jsx   # Admin control panel
│   │   │   ├── ChatMessageViewer.jsx # Message display
│   │   │   ├── ChatSideBar.jsx      # Chat list sidebar
│   │   │   ├── Home.jsx             # Landing page
│   │   │   ├── Login.jsx            # Login page
│   │   │   ├── NLtoSQL.jsx          # NL to SQL converter
│   │   │   ├── Profile.jsx          # User profile editor
│   │   │   ├── RewriteSql.jsx       # SQL rewrite interface
│   │   │   └── Signup.jsx           # Registration page
│   │   │
│   │   ├── styles/
│   │   │   ├── admin.css            # Admin dashboard styles
│   │   │   ├── chatbar.css          # Chat sidebar styles
│   │   │   ├── home.css             # Home page styles
│   │   │   ├── loginsignup.css      # Auth pages styles
│   │   │   ├── nltosql.css          # NL to SQL page styles
│   │   │   ├── rewrite.css          # Rewrite page styles
│   │   │   └── usermenu.css         # User menu styles
│   │   │
│   │   ├── App.css                  # Global styles
│   │   ├── App.jsx                  # Root component with routing
│   │   ├── index.css                # Base CSS imports
│   │   └── main.jsx                 # React entry point
│   │
│   ├── .gitignore                   # Git ignore file
│   ├── eslint.config.js             # ESLint configuration
│   ├── index.html                   # HTML entry point
│   ├── package-lock.json            # npm lock file
│   ├── package.json                 # npm configuration
│   ├── postcss.config.js            # PostCSS configuration
│   ├── README.md                    # Frontend documentation
│   ├── tailwind.config.js           # Tailwind CSS config
│   └── vite.config.js               # Vite config with HTTPS
│
├── postgres/
│   ├── .gitignore                   # PostgreSQL gitignore
│   └── docker-compose.yml           # PostgreSQL container setup
│
└── README.md                        # Main project documentation
```

---

## ⚙️ Tech Stack

### Backend
- **FastAPI** – Modern Python web framework
- **PostgreSQL** – Relational database
- **Google Gemini 2.5 Flash** – LLM for SQL generation
- **bcrypt** – Password hashing
- **Fernet (cryptography)** – AES-256 encryption
- **SlowAPI** – Rate limiting middleware
- **Uvicorn** – ASGI server with HTTPS support
- **PyJWT** – JWT token management

### Frontend
- **React** – UI library
- **Vite** – Build tool and dev server
- **Axios** – HTTP client with interceptors
- **React Router** – Client-side routing
- **Prism.js** – SQL syntax highlighting
- **Tailwind CSS** – Utility-first styling
- **Custom CSS** – Component-specific styles
- **ESLint** – Code quality and linting

---

## 🔐 Security Architecture

### Data Encryption (AES-256)

Encrypted at rest in PostgreSQL:
- User email addresses
- User biography text
- All chat messages (both user prompts and AI responses)

```python
# Encryption flow
plaintext → AES-256-CBC → base64 → database
database → base64 decode → AES-256-CBC decrypt → plaintext
```

### Response Integrity (HMAC-SHA256)

Every LLM endpoint response includes a signature:

```json
{
  "data": {
    "sql": "SELECT ...",
    "explanation": "..."
  },
  "signature": "a1b2c3d4e5f6..."
}
```

Frontend verifies signature before using response. If tampered, displays: **"Response integrity check failed"**

### Rate Limiting

| Endpoint | Limit | Purpose |
|----------|-------|---------|
| `/rewrite-sql` | 5 per minute | Prevent API abuse |
| `/nl-to-sql` | 10 per minute | Protect LLM quota |

### Authentication Flow

1. User logs in → backend generates JWT
2. Frontend stores token in memory/localStorage
3. Axios interceptor adds `Authorization: Bearer <token>` to all requests
4. Backend validates JWT on protected routes
5. Token refresh logic handles expiration

### SQL Safety

- Parameterized queries prevent injection
- Safety filters validate generated SQL
- Blacklist checks for dangerous keywords
- Execution in read-only context when possible

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (or Docker)
- Google Gemini API key

---

### Backend Setup

#### 1️⃣ Create virtual environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2️⃣ Install dependencies

```bash
pip install -r requirement.txt
```

#### 3️⃣ Create `.env` file

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=yourpassword
DB_NAME=promptsmith

# Security Keys
JWT_SECRET=your_jwt_secret_key_min_32_chars
AES_KEY=your_32_byte_aes_key_base64_encoded
HMAC_SECRET=your_hmac_secret_key

# LLM Configuration
GEMINI_API_KEY=your_google_gemini_api_key

# Server Configuration
BACKEND_URL=https://localhost:8000
FRONTEND_URL=https://localhost:5173
```

**Generate secure keys:**

```python
# AES Key (32 bytes)
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())

# JWT/HMAC Secret
import secrets
print(secrets.token_urlsafe(32))
```

#### 4️⃣ Start PostgreSQL

Using Docker:

```bash
cd postgres
docker-compose up -d
```

Or install PostgreSQL locally and create database:

```sql
CREATE DATABASE promptsmith;
```

#### 5️⃣ Generate SSL certificates (for local HTTPS)

```bash
cd backend
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365
```

#### 6️⃣ Run backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 \
  --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

Backend accessible at: **https://localhost:8000**

API docs at: **https://localhost:8000/docs**

---

### Frontend Setup

#### 1️⃣ Install dependencies

```bash
cd frontend
npm install
```

#### 2️⃣ Configure environment

Update `src/api/axiosAuth.js` if needed:

```javascript
const API_BASE_URL = 'https://localhost:8000';
```

#### 3️⃣ Run development server

```bash
npm run dev
```

Frontend runs at: **https://localhost:5173**

---

## 🧪 Testing Features

### Test NL→SQL Conversion

1. Create account and login
2. Navigate to "NL to SQL" page
3. Try example queries:
   - "Show me last 30 days revenue by customer in descending order"
   - "Find top 10 products by sales this quarter"
   - "List all active users who signed up this month"

### Test SQL Rewrite

1. Navigate to "Rewrite SQL" (no login required)
2. Paste unformatted SQL:
   ```sql
   select*from users where id=1
   ```
3. Receive formatted result:
   ```sql
   SELECT *
   FROM users
   WHERE id = 1;
   ```

### Test HMAC Integrity

1. Open browser DevTools → Network tab
2. Intercept response from `/nl-to-sql`
3. Modify the `signature` field
4. Frontend should display: **"Response integrity check failed"**

### Test Encryption

1. Login and send chat messages
2. Check PostgreSQL database directly:
   ```sql
   SELECT message, ai_response FROM chats LIMIT 1;
   ```
3. Values should be unreadable (base64-encoded AES ciphertext)

### Test Admin Dashboard

1. Create admin user (manually set `is_admin=true` in DB)
2. Login as admin
3. Access admin dashboard to:
   - View all users
   - See system analytics
   - Manage user chats
   - Disable users

---

## 📊 Admin Analytics Dashboard

The admin panel displays real-time system metrics:

**User Metrics:**
- 👥 Total registered users
- 🟢 Active users (not disabled)
- 📈 User growth over time

**Chat Metrics:**
- 💬 Total chat sessions
- 📝 Total messages exchanged
- 🔄 Average messages per chat

**API Usage:**
- 🤖 NL→SQL request count
- 🛠 Rewrite-SQL request count
- 📊 Daily/weekly usage trends

**User Management:**
- View detailed user list with registration dates
- Access any user's complete chat history
- Soft-delete users (disable instead of permanent deletion)
- Monitor user activity patterns

---

## 🔧 Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASS` | Database password | `secure_password` |
| `DB_NAME` | Database name | `promptsmith` |
| `JWT_SECRET` | JWT token signing | `random_32_char_string` |
| `AES_KEY` | AES-256 encryption key | `base64_encoded_32_bytes` |
| `HMAC_SECRET` | Response signature key | `random_secret_string` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |
| `BACKEND_URL` | Backend base URL | `https://localhost:8000` |
| `FRONTEND_URL` | Frontend base URL | `https://localhost:5173` |

---

## 📦 Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

Output in `frontend/dist/`

### Deploy Backend

1. Use proper SSL certificates (Let's Encrypt)
2. Set environment variables securely
3. Use production ASGI server (Gunicorn + Uvicorn)
4. Enable CORS for production domain only
5. Set up database backups

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:443 --keyfile=/path/to/key.pem --certfile=/path/to/cert.pem
```

### Serve with Reverse Proxy

Use Nginx or Caddy:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass https://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎯 Why This Project Stands Out

**Academic Excellence:**
- Demonstrates comprehensive security knowledge
- Real-world encryption and signing implementation
- Production-grade architecture and design patterns
- Complete full-stack integration

**Technical Depth:**
- AES-256 encryption with proper key management
- HMAC signature verification
- JWT authentication with refresh logic
- SQL injection prevention
- Rate limiting for API protection

**Feature Completeness:**
- User authentication and authorization
- Role-based access control (admin/user)
- Real-time chat system with history
- Admin dashboard with system analytics
- Public and authenticated API endpoints

**Best Practices:**
- HTTPS everywhere
- Environment-based configuration
- Proper error handling
- Clean code organization
- Comprehensive documentation

---

## 🏆 Project Credits

**Developed by:** Paras Sachdeva  
**Institution:** Purdue University  
**Course:** Secure Web Application Development (2025)  
**Purpose:** Academic project demonstrating production-grade security practices in AI-powered web applications

---

## 📝 License

MIT License - Free to use for educational and commercial purposes.

---

## 🤝 Contributing

This is an academic project, but feedback and suggestions are welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Email: parassa1006@gmail.com
- Project documentation: `/docs`

---

## 🔍 File Structure Summary

### Backend Components

**Routes (API Endpoints):**
- `admin_routes.py` - Admin dashboard and management
- `auth.py` - Authentication and user management
- `chat_routes.py` - Chat CRUD operations

**Services (Business Logic):**
- `correctness.py` - SQL validation and correctness checks
- `sql_executor.py` - Safe SQL execution wrapper

**Utils (Helper Functions):**
- `db.py` - Database connection management
- `hmac_sign.py` - HMAC signature utilities
- `rate_limiter.py` - Rate limiting configuration
- `sql_executor.py` - SQL execution helpers

### Frontend Components

**API Layer:**
- `auth.js` - Authentication API calls
- `axiosAuth.js` - Axios configuration with JWT interceptor

**Components:**
- `helperComponents.jsx` - Reusable UI elements
- `UserMenu.jsx` - User dropdown navigation

**Pages:**
- `AdminDashboard.jsx` - Admin control panel
- `ChatMessageViewer.jsx` - Chat message display
- `ChatSideBar.jsx` - Chat navigation sidebar
- `Home.jsx` - Landing page
- `Login.jsx` - User login
- `NLtoSQL.jsx` - Natural language to SQL converter
- `Profile.jsx` - User profile management
- `RewriteSql.jsx` - SQL rewrite tool
- `Signup.jsx` - User registration

**Styles:**
- Modular CSS files for each major component
- Tailwind CSS integration
- Custom styling system

---

**Built with ❤️ using FastAPI, React, and Google Gemini**
