from fastapi import APIRouter, Depends, HTTPException
from utils.db import get_connection as get_db
from psycopg2.extras import RealDictCursor
from routes.auth import require_user
from fastapi.security import HTTPBearer

# AES Encryption
from utils.encryption import encrypt_text, decrypt_text

router = APIRouter()
bearer_scheme = HTTPBearer()


# ----------------------------
# CREATE NEW CHAT
# ----------------------------
@router.post("/chats/create")
def create_chat(user=Depends(require_user), db=Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)

    encrypted_title = encrypt_text("New Chat")

    cur.execute(
        "INSERT INTO chats (user_id, title) VALUES (%s, %s) RETURNING id",
        (user["id"], encrypted_title)
    )
    row = cur.fetchone()
    db.commit()

    return {"chat_id": row["id"]}


# ----------------------------
# LIST CHATS
# ----------------------------
@router.get("/chats/list")
def get_chats(user=Depends(require_user), db=Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT id, title, updated_at FROM chats WHERE user_id=%s ORDER BY updated_at DESC",
        (user["id"],)
    )
    rows = cur.fetchall()

    # Decrypt chat titles
    for r in rows:
        if r["title"]:
            try:
                r["title"] = decrypt_text(r["title"])
            except Exception:
                # If decryption fails, keep plaintext title
                pass

    return rows


# ----------------------------
# SAVE MESSAGE (NL-to-SQL)
# ----------------------------
def save_message(chat_id, user_msg, ai_msg, raw_sql, final_sql, db):
    cur = db.cursor()

    enc_user_msg = encrypt_text(user_msg)
    enc_ai_msg = encrypt_text(ai_msg)
    enc_raw = encrypt_text(raw_sql)
    enc_final = encrypt_text(final_sql)

    cur.execute(
        """
        INSERT INTO chat_messages (chat_id, user_message, ai_response, raw_sql, final_sql)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (chat_id, enc_user_msg, enc_ai_msg, enc_raw, enc_final)
    )

    cur.execute("UPDATE chats SET updated_at = NOW() WHERE id=%s", (chat_id,))
    db.commit()


# ----------------------------
# GET MESSAGES FOR A CHAT
# ----------------------------
@router.get("/chats/{chat_id}/messages")
def get_chat_messages(chat_id: int, user=Depends(require_user), db=Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)

    # Verify chat belongs to user
    cur.execute("SELECT id, title FROM chats WHERE id=%s AND user_id=%s", (chat_id, user["id"]))
    chat_row = cur.fetchone()

    if not chat_row:
        raise HTTPException(404, "Chat not found")

    # Decrypt chat title
    try:
        chat_row["title"] = decrypt_text(chat_row["title"])
    except Exception:
        pass

    # Fetch messages
    cur.execute(
        """
        SELECT id, user_message, ai_response, raw_sql, final_sql, created_at
        FROM chat_messages
        WHERE chat_id=%s
        ORDER BY created_at ASC
        """,
        (chat_id,)
    )
    rows = cur.fetchall()

    # Decrypt every message field
    for msg in rows:
        if msg["user_message"]:
            try:
                msg["user_message"] = decrypt_text(msg["user_message"])
            except Exception:
                pass
        if msg["ai_response"]:
            try:
                msg["ai_response"] = decrypt_text(msg["ai_response"])
            except Exception:
                pass
        if msg["raw_sql"]:
            try:
                msg["raw_sql"] = decrypt_text(msg["raw_sql"])
            except Exception:
                pass
        if msg["final_sql"]:
            try:
                msg["final_sql"] = decrypt_text(msg["final_sql"])
            except Exception:
                pass

    return {
        "chat": chat_row,
        "messages": rows
    }


# ----------------------------
# DELETE A CHAT
# ----------------------------
@router.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, user = Depends(require_user), db=Depends(get_db)):
    cur = db.cursor()

    # Ensure the chat belongs to the user
    cur.execute("SELECT id FROM chats WHERE id = %s AND user_id = %s", (chat_id, user["id"]))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Chat not found")

    # Delete messages first due to FK constraints
    cur.execute("DELETE FROM chat_messages WHERE chat_id = %s", (chat_id,))
    cur.execute("DELETE FROM chats WHERE id = %s", (chat_id,))
    
    db.commit()
    cur.close()

    return {"success": True, "deleted_chat": chat_id}