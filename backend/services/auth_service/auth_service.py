import bcrypt
from utils.db import get_connection

# ---------------------
# PASSWORD HASHING
# ---------------------

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------------
# DATABASE HELPERS
# ---------------------

def find_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cur.fetchone()

def create_user(name: str, email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    hashed = hash_password(password)

    cur.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, name, email, role;
        """,
        (name, email, hashed)
    )

    conn.commit()
    return cur.fetchone()

def update_profile(user_id: int, name: str, bio: str, profile_image: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name=%s, bio=%s, profile_image=%s
        WHERE id=%s
        RETURNING id, email, name, role, bio, profile_image;
    """, (name, bio, profile_image, user_id))

    conn.commit()
    return cur.fetchone()

def get_profile(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, name, role, bio, profile_image, created_at
        FROM users
        WHERE id=%s;
    """, (user_id,))

    return cur.fetchone()
