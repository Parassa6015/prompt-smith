import ollama
from utils.sql_executor import run_sql
from utils.correctness import compare_results

PRIMARY_MODEL = "sqlcoder"
FALLBACK_MODEL = "llama3.2:3b"

DEFAULT_INSTRUCTION = (
    "Rewrite the SQL to improve performance while keeping results identical. "
    "STRICT RULES: Do NOT remove column aliases. Preserve all SELECT column names exactly. "
    "Do NOT simplify aggregates or remove AS clauses. "
    'Output only the rewritten SQL.'
)


def rewrite_with_model(model, sql, instruction):
    prompt = f"""
Rewrite the following SQL query into a more efficient version.
Rules:
- Must return the same result set.
- Do not change the meaning.
- Do not add explanations.
- Output only the rewritten SQL.

Instruction: {instruction}

Query:
{sql}
"""

    try:
        response = ollama.generate(
            model=model,
            prompt=prompt
        )
        return response["response"].strip()
    except Exception as e:
        return f"ERROR: {str(e)}"


def rewrite_sql_pipeline(sql):
    # 1. Try primary model (sqlcoder)
    rewritten = rewrite_with_model(PRIMARY_MODEL, sql, DEFAULT_INSTRUCTION)

    # Check validity
    if rewritten.startswith("ERROR") or not run_sql(rewritten)["success"]:
        # 2. Try fallback (llama3)
        rewritten = rewrite_with_model(FALLBACK_MODEL, sql, DEFAULT_INSTRUCTION)

    # 3. correctness check
    original_res = run_sql(sql)
    rewritten_res = run_sql(rewritten)
    comparison = compare_results(original_res, rewritten_res)

    return {
        "original": original_res,
        "rewritten_sql": rewritten,
        "rewritten_result": rewritten_res,
        "comparison": comparison
    }
