from fastapi import APIRouter, Depends, HTTPException
from utils.db import get_connection as get_db
from routes.auth import require_user
from psycopg2.extras import RealDictCursor
from utils.encryption import decrypt_text
from utils.encryption import encrypt_text  # if needed for future updates

router = APIRouter(prefix="/admin", tags=["Admin"])


# -----------------------------
# Helper: Require admin role
# -----------------------------
def require_admin(user):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return True


# -----------------------------
# 1) LIST ALL USERS
# -----------------------------
@router.get("/users")
def list_users(user=Depends(require_user), db=Depends(get_db)):
    require_admin(user)

    cur = db.cursor(cursor_factory=RealDictCursor)
    # Exclude the current admin from the list
    cur.execute(
        "SELECT id, name, email, role, bio, avatar_emoji FROM users WHERE id != %s ORDER BY id",
        (user["id"],)
    )
    rows = cur.fetchall()

    # decrypt sensitive fields
    for r in rows:
        r["email"] = decrypt_text(r["email"])
        if r["bio"]:
            r["bio"] = decrypt_text(r["bio"])

    cur.close()
    return rows


# -----------------------------
# 2) DELETE A USER
# -----------------------------
@router.delete("/users/{user_id}")
def delete_user(user_id: int, user=Depends(require_user), db=Depends(get_db)):
    require_admin(user)  # Check admin after getting user
    
    if user_id == user["id"]:
        raise HTTPException(400, "Cannot delete your own account")

    cur = db.cursor()

    # Delete messages first
    cur.execute("""
        DELETE FROM chat_messages 
        WHERE chat_id IN (SELECT id FROM chats WHERE user_id = %s)
    """, (user_id,))

    # Delete chats
    cur.execute("DELETE FROM chats WHERE user_id = %s", (user_id,))

    # Delete user
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

    db.commit()
    cur.close()

    return {"success": True, "message": "User and all related data deleted."}

# -----------------------------
# 3) LIST CHATS OF A USER
# -----------------------------
@router.get("/users/{user_id}/chats")
def get_user_chats(user_id: int, user=Depends(require_user), db=Depends(get_db)):
    require_admin(user)

    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT id, title, updated_at FROM chats WHERE user_id = %s ORDER BY updated_at DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    return rows


# -----------------------------
# 4) DELETE A CHAT
# -----------------------------
@router.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, user=Depends(require_user), db=Depends(get_db)):
    require_admin(user)

    cur = db.cursor()

    # delete messages first
    cur.execute("DELETE FROM chat_messages WHERE chat_id = %s", (chat_id,))
    # delete the chat itself
    cur.execute("DELETE FROM chats WHERE id = %s", (chat_id,))

    db.commit()
    cur.close()

    return {"success": True, "message": "Chat deleted"}


# -----------------------------
# 5) ANALYTICS DASHBOARD
# -----------------------------
@router.get("/analytics")
def get_analytics(user=Depends(require_user), db=Depends(get_db)):
    require_admin(user)  # Check admin after getting user
    
    cur = db.cursor()

    # total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # total chats
    cur.execute("SELECT COUNT(*) FROM chats")
    total_chats = cur.fetchone()[0]

    # total messages
    cur.execute("SELECT COUNT(*) FROM chat_messages")
    total_messages = cur.fetchone()[0]

    # For LLM usage, use messages count since llm_usage table doesn't exist
    # Each message represents an LLM call
    llm_usage = total_messages

    cur.close()

    return {
        "total_users": total_users,
        "total_chats": total_chats,
        "total_messages": total_messages,
        "llm_usage": llm_usage
    }
