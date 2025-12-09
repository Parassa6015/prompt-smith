from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from utils.db import get_connection as get_db
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from psycopg2.extras import RealDictCursor
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import random
router = APIRouter()

# JWT Configuration - Use environment variable in production
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret123")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# Security schemes
bearer_scheme = HTTPBearer()



EMOJI_LIST = [
    "🦊","🐼","🐧","🐯","🐸","🐨","🐳","🐙","🐢",
    "🦁","🐶","🐱","🐻","🐰","🐹","🐼","🐵",
]



# ========================
# Pydantic Models
# ========================
class SignupModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

class UpdateProfileModel(BaseModel):
    name: str | None = None
    password: str | None = None

# ========================
# Helper Functions
# ========================
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt(payload: dict):
    """Create a JWT token with expiration"""
    data = payload.copy()
    data["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str):
    """Decode and verify a JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ========================
# Dependency Functions
# ========================
def require_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db=Depends(get_db)):
    """Protect routes that require authentication"""
    payload = decode_jwt(credentials.credentials)
    user_id = payload.get("user_id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # Fetch user from database
    cur = db.cursor()
    cur.execute("SELECT id, name, email, role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "role": row["role"]
    }

def require_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db=Depends(get_db)):
    """Protect admin-only routes"""
    user = require_user(credentials, db)
    
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")
    
    return user

# ========================
# Routes
# ========================
@router.post("/signup")
def signup(data: SignupModel, db=Depends(get_db)):
    cur = db.cursor()

    # Check email
    cur.execute("SELECT id FROM users WHERE email=%s", (data.email,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    # Pick avatar emoji
    avatar = pick_random_emoji()

    cur.execute(
        """
        INSERT INTO users (name, email, password_hash, avatar_emoji)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (data.name, data.email, hashed, avatar)
    )

    row = cur.fetchone()
    db.commit()

    return { "success": True, "user_id": row[0] }


def pick_random_emoji():
    return random.choice(EMOJI_LIST)

@router.post("/login")
def login(data: LoginModel, db=Depends(get_db)):
    """Authenticate user and return JWT token"""
    cur = db.cursor()

    cur.execute(
        "SELECT id, password_hash, name, email, role FROM users WHERE email=%s",
        (data.email,)
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(data.password, row["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create JWT token
    token = create_jwt({
        "user_id": row["id"],
        "role": row["role"]
    })

    return {
        "success": True,
        "token": token,
        "user": {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "role": row["role"],
        }
    }


@router.get("/profile")
def get_profile(user = Depends(require_user), db=Depends(get_db)):
    """Get current user profile"""
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, email, role, avatar_emoji FROM users WHERE id=%s", (user["id"],))
    row = cur.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return row


@router.post("/profile/update")
def update_profile(
    data: UpdateProfileModel,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db=Depends(get_db)
):
    """Update current user's profile"""
    payload = decode_jwt(credentials.credentials)
    user_id = payload.get("user_id")
    
    cur = db.cursor()

    # Update name if provided
    if data.name:
        cur.execute("UPDATE users SET name=%s WHERE id=%s", (data.name, user_id))

    # Update password if provided
    if data.password:
        hashed = hash_password(data.password)
        cur.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hashed, user_id))

    db.commit()

    return {"success": True, "message": "Profile updated"}