from fastapi import FastAPI
from utils.db import get_connection

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/db-test")
def db_test():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 AS test;")
        result = cur.fetchone()
        conn.close()
        return {"status": "connected", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
