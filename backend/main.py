from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.llm_service import rewrite_sql_pipeline
from services.instruction_search import find_best_instruction
from services.nl_to_sql_service import generate_sql_from_prompt
from utils.sql_executor import run_sql

app = FastAPI(
    title="PromptSmith Backend",
    description="SQL rewrite engine with LLM model selection",
    version="1.0.0"
)

class RewriteSQLRequest(BaseModel):
    query: str

class NLQuery(BaseModel):
    prompt: str

class InstructionSearchRequest(BaseModel):
    query: str
    attempts: int = 3


@app.get("/")
def root():
    return {"status": "running", "message": "PromptSmith backend online"}


@app.post("/rewrite-sql")
def rewrite_sql(req: RewriteSQLRequest):
    return rewrite_sql_pipeline(req.query)


@app.post("/find-instruction")
def find_instruction(req: InstructionSearchRequest):
    return find_best_instruction(req.query, req.attempts)


@app.post("/nl-to-sql")
def nl_to_sql(body: NLQuery):
    prompt = body.prompt
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    # 1. Generate SQL from NL
    raw_sql = generate_sql_from_prompt(prompt)

    # 2. Rewrite the SQL safely
    rewrite_result = rewrite_sql_pipeline(raw_sql)
    final_sql = rewrite_result["rewritten_sql"]

    # 3. Execute rewritten SQL
    sql_res = run_sql(final_sql)

    return {
        "generated_sql": raw_sql,
        "final_sql": final_sql,
        "result": sql_res
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)