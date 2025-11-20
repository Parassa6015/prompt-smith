from fastapi import FastAPI
from utils.db import get_connection
from pydantic import BaseModel
from utils.sql_executor import run_sql
from utils.correctness import compare_results
from services.llm_service import rewrite_sql_pipeline
from services.instruction_search import find_best_instruction


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
class SQLQuery(BaseModel):
    query: str

@app.post("/execute-sql")
def execute_sql(payload: SQLQuery):
    result = run_sql(payload.query)
    return result
class SQLPair(BaseModel):
    original: str
    rewritten: str

@app.post("/check-correctness")
def check_correctness(payload: SQLPair):
    original_res = run_sql(payload.original)
    rewritten_res = run_sql(payload.rewritten)

    comparison = compare_results(original_res, rewritten_res)

    return {
        "original": original_res,
        "rewritten": rewritten_res,
        "comparison": comparison
    }

class RewriteRequest(BaseModel):
    query: str

@app.post("/rewrite-sql")
def rewrite_sql(payload: RewriteRequest):
    return rewrite_sql_pipeline(payload.query)

class SearchRequest(BaseModel):
    query: str

@app.post("/instruction-search")
def instruction_search(payload: SearchRequest):
    return find_best_instruction("sqlcoder", payload.query)

