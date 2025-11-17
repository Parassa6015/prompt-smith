import time
from utils.db import get_connection

def run_sql(query: str):
    try:
        conn = get_connection()
        cur = conn.cursor()

        start = time.time()
        if not query.strip().endswith(";"):
            query = query.strip() + ";"
        cur.execute(query)
        
        # Convert rows to normal Python dicts
        rows = [dict(r) for r in cur.fetchall()]
        
        end = time.time()

        columns = [desc[0] for desc in cur.description]

        conn.commit()
        conn.close()

        return {
            "success": True,
            "rows": rows,
            "columns": columns,
            "time_ms": round((end - start) * 1000, 3)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "rows": [],
            "columns": [],
            "time_ms": None
        }

