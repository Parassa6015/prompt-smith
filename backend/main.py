from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()
print(f"🔑 HMAC_SECRET_KEY from env: {os.getenv('HMAC_SECRET_KEY', 'NOT FOUND')}")


import traceback
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
from utils.hmac_sign import generate_signature
from utils.rate_limiter import rate_limit
from routes import admin_routes

# Import authentication dependencies
from routes import auth
from routes.auth import require_user, require_admin

app = FastAPI(
    title="PromptSmith Backend",
    description="SQL rewrite engine with LLM model selection",
    version="1.0.0"
)
origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "http://127.0.0.1:5173",
    "https://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router)
app.include_router(chat_routes.router)
app.include_router(admin_routes.router)

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
    rate_limit(user["id"], endpoint="rewrite_sql")
    result = rewrite_sql_pipeline(req.query)
    
    # Handle different return types from rewrite_sql_pipeline
    if isinstance(result, dict):
        # If it returns a dict, try to extract the SQL string
        if 'rewritten_sql' in result:
            # If it's nested, extract it
            rewritten_data = result['rewritten_sql']
            if isinstance(rewritten_data, str):
                rewritten = rewritten_data
            elif isinstance(rewritten_data, dict):
                # If still a dict, check for common SQL keys
                rewritten = (
                    rewritten_data.get('sql') or 
                    rewritten_data.get('query') or 
                    str(rewritten_data)
                )
            else:
                rewritten = str(rewritten_data)
        else:
            # No 'rewritten_sql' key, convert entire result
            rewritten = str(result)
    else:
        # If it's already a string or other type
        rewritten = str(result)
    
    signed = {
        "rewritten_sql": rewritten,
    }

    print("Data being signed:", signed)
    signature = generate_signature(signed)
    print("Generated signature:", signature)

    return {
        "data": signed,
        "signature": signature
    }

@app.post("/find-instruction")
def find_instruction(req: InstructionSearchRequest, user: dict = Depends(require_user)):
    """Find best instruction for a given query"""
    rate_limit(user["id"], endpoint="find_instruction")
    return find_best_instruction(req.query, req.attempts)


@app.post("/nl-to-sql")
def nl_to_sql(body: NLQuery, user: dict = Depends(require_user), db=Depends(get_db)):
    rate_limit(user["id"], endpoint="nl_to_sql")
    try:
        
        prompt = body.prompt
        model: Optional[str] = "Gemini Flash 2.5"

        # First safety check
        if not is_prompt_safe(prompt):
            raise HTTPException(400, "This natural-language request is not allowed.")

        # Generate SQL
        try:
            raw_sql = generate_sql_from_prompt(prompt)
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                raise HTTPException(
                    429, 
                    "API quota exceeded. Please try again later or use the Ollama model option."
                )
            raise

        # Validate SQL
        if not is_sql_safe(raw_sql):
            raise HTTPException(400, "Unsafe SQL detected")

        # Rewrite SQL
        rewrite_result = rewrite_sql_pipeline(raw_sql)
        
        # Extract the final SQL string properly
        if isinstance(rewrite_result, dict) and 'rewritten_sql' in rewrite_result:
            final_sql_data = rewrite_result['rewritten_sql']
            if isinstance(final_sql_data, str):
                final_sql = final_sql_data
            else:
                final_sql = str(final_sql_data)
        else:
            final_sql = str(rewrite_result)

        # Execute SQL
        sql_res = run_sql(final_sql)

        # Create chat if not exists
        if body.chat_id is None:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO chats (user_id, title) VALUES (%s, %s) RETURNING id",
                (user["id"], prompt[:50])
            )
            result = cur.fetchone()
            chat_id = result["id"] if isinstance(result, dict) else result[0]
            db.commit()
        else:
            chat_id = body.chat_id

        # Save history
        save_message(
            chat_id=chat_id,
            user_msg=prompt,
            ai_msg=str(sql_res),
            raw_sql=raw_sql,
            final_sql=final_sql,
            db=db
        )

        # Prepare payload with proper serialization
        payload = {
            "generated_sql": raw_sql,
            "final_sql": final_sql,
            "result": sql_res,
            "chat_id": chat_id
        }

        signature = generate_signature(payload)

        return {
            "data": payload,
            "signature": signature
        }

    except HTTPException:
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(500, f"Error: {str(e)}")


@app.get("/admin/dashboard")
def admin_dashboard(admin: dict = Depends(require_admin)):
    """Admin-only dashboard endpoint"""
    return {
        "message": f"Welcome Admin {admin['name']}!",
        "admin": admin
    }




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_certfile="cert.pem",
        ssl_keyfile="key.pem",
        reload=True
    )