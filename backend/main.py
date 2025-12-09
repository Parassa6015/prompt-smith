from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

from services.llm_service import rewrite_sql_pipeline
from services.instruction_search import find_best_instruction
from services.nl_to_sql_service import generate_sql_from_prompt
from utils.sql_executor import run_sql
from services.sql_validator import validate_sql
from services.cleaner import is_prompt_safe
from services.sql_validator import is_sql_safe
from routes.chat_routes import save_message
from routes import chat_routes
from utils.db import get_connection as get_db

# Import authentication dependencies
from routes import auth
from routes.auth import require_user, require_admin

app = FastAPI(
    title="PromptSmith Backend",
    description="SQL rewrite engine with LLM model selection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router)
app.include_router(chat_routes.router)

# ========================
# Pydantic Models
# ========================
class RewriteSQLRequest(BaseModel):
    query: str

class NLQuery(BaseModel):
    prompt: str
    chat_id: int | None = None

class InstructionSearchRequest(BaseModel):
    query: str
    attempts: int = 3

# ========================
# Routes
# ========================
@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "running", "message": "PromptSmith backend online"}


@app.post("/rewrite-sql")
def rewrite_sql(req: RewriteSQLRequest, user: dict = Depends(require_user)):
    """Rewrite SQL query using LLM pipeline"""
    return rewrite_sql_pipeline(req.query)


@app.post("/find-instruction")
def find_instruction(req: InstructionSearchRequest, user: dict = Depends(require_user)):
    """Find best instruction for a given query"""
    return find_best_instruction(req.query, req.attempts)


@app.post("/nl-to-sql")
def nl_to_sql(body: NLQuery, user: dict = Depends(require_user), db=Depends(get_db)):
    """Convert natural language to SQL"""
    try:
        prompt = body.prompt
        model: Optional[str] = "Gemini Flash 2.5"

        # First safety check: validate the prompt
        if not is_prompt_safe(prompt):
            raise HTTPException(
                status_code=400,
                detail="This natural-language request is not allowed. Dangerous modification intent detected."
            )

        # Generate SQL from natural language
        raw_sql = generate_sql_from_prompt(prompt)

        # Second safety check: validate generated SQL
        if not is_sql_safe(raw_sql):
            raise HTTPException(
                status_code=400,
                detail="Unsafe SQL detected"
            )

        # Rewrite and execute SQL
        rewrite_result = rewrite_sql_pipeline(raw_sql)
        final_sql = rewrite_result["rewritten_sql"]
        
        sql_res = run_sql(final_sql)
        
        # Create new chat if chat_id not provided
        if body.chat_id is None:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO chats (user_id, title) VALUES (%s, %s) RETURNING id",
                (user["id"], prompt[:50])
            )
            result = cur.fetchone()
            chat_id = result['id'] if isinstance(result, dict) else result[0]
            db.commit()
        else:
            chat_id = body.chat_id
        
        save_message(
            chat_id=chat_id,
            user_msg=prompt,
            ai_msg=str(sql_res),
            raw_sql=raw_sql,
            final_sql=final_sql,
            db=db
        )

        return {
            "generated_sql": raw_sql,
            "final_sql": final_sql,
            "result": sql_res,
            "chat_id": chat_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("ERROR in nl_to_sql:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )

@app.get("/admin/dashboard")
def admin_dashboard(admin: dict = Depends(require_admin)):
    """Admin-only dashboard endpoint"""
    return {
        "message": f"Welcome Admin {admin['name']}!",
        "admin": admin
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)