from fastapi import APIRouter, Depends, HTTPException
from utils.db import get_connection as get_db
import os
from psycopg2.extras import RealDictCursor
from fastapi.security import HTTPBearer
from routes.auth import require_user
router = APIRouter()


# Security schemes
bearer_scheme = HTTPBearer()

@router.post("/chats/create")
def create_chat(user=Depends(require_user), db=Depends(get_db)):
    # Use RealDictCursor to get dictionary results
    cur = db.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "INSERT INTO chats (user_id) VALUES (%s) RETURNING id",
        (user["id"],)
    )

    row = cur.fetchone()
    if not row:
        raise HTTPException(500, "Did not receive chat_id from database")

    chat_id = row["id"]

    db.commit()
    cur.close()

    return {"chat_id": chat_id}


@router.get("/chats/list")
def get_chats(user = Depends(require_user), db=Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM chats WHERE user_id = %s ORDER BY updated_at DESC", (user["id"],))
    results = cur.fetchall()
    cur.close()
    return results

def save_message(chat_id, user_msg, ai_msg, raw_sql, final_sql, db):
    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO chat_messages (chat_id, user_message, ai_response, raw_sql, final_sql)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (chat_id, user_msg, ai_msg, raw_sql, final_sql)
    )
    cur.execute("UPDATE chats SET updated_at = NOW() WHERE id = %s", (chat_id,))
    db.commit()
    cur.close()

@router.get("/chats/{chat_id}/messages")
def get_chat_messages(chat_id: int, user=Depends(require_user), db=Depends(get_db)):
    cur = db.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM chats WHERE id=%s AND user_id=%s", (chat_id, user["id"]))
    if not cur.fetchone():
        cur.close()
        raise HTTPException(404, "Chat not found")

    cur.execute(
        "SELECT * FROM chat_messages WHERE chat_id=%s ORDER BY created_at ASC",
        (chat_id,)
    )
    results = cur.fetchall()
    cur.close()
    return results

@router.delete("/chats/{chat_id}/delete")
def delete_chat(chat_id: int, user=Depends(require_user), db=Depends(get_db)):
    cur = db.cursor()

    # Ensure the chat belongs to the user
    cur.execute("SELECT id FROM chats WHERE id=%s AND user_id=%s", (chat_id, user["id"]))
    if not cur.fetchone():
        raise HTTPException(404, "Chat not found")

    # Delete messages then chat
    cur.execute("DELETE FROM chat_messages WHERE chat_id=%s", (chat_id,))
    cur.execute("DELETE FROM chats WHERE id=%s", (chat_id,))
    db.commit()

    return {"success": True}