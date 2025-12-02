# import ollama
# from utils.sql_executor import run_sql
# from utils.correctness import compare_results

# PRIMARY_MODEL = "sqlcoder:15b"   # for 8GB RAM laptop
# FALLBACK_MODEL = None

# def clean_sql(raw):
#     if not raw:
#         return raw
#     return (
#         raw.replace("<s>", "")
#            .replace("</s>", "")
#            .replace("```sql", "")
#            .replace("```", "")
#            .strip()
#     )


# DEFAULT_INSTRUCTION = (
#     "Rewrite the SQL ONLY for formatting and performance while keeping the query EXACTLY the same. "
#     "STRICT RULES:\n"
#     "- Do NOT change the logic of the query.\n"
#     "- Do NOT add or remove columns.\n"
#     "- Do NOT rename or modify column aliases.\n"
#     "- Do NOT reorder SELECT columns.\n"
#     "- Do NOT introduce JOINs if the original used subqueries.\n"
#     "- Do NOT remove subqueries or convert them into joins.\n"
#     "- Do NOT add window functions, GROUP BY, HAVING, ORDER BY, DISTINCT, or aggregates that do not exist.\n"
#     "- Do NOT reorder GROUP BY or HAVING clauses unless identical.\n"
#     "- Do NOT add filters, remove filters, or change filter logic.\n"
#     "- Do NOT rewrite the structure of the query.\n"
#     "- Do NOT invent or use columns that do not exist in the original SQL.\n"
#     "- Maintain all WHERE, GROUP BY, HAVING, ORDER BY clauses exactly.\n"
#     "- Maintain all parentheses, nested subqueries, and expressions.\n"
#     "- Output ONLY the rewritten SQL. NO markdown, NO backticks, NO explanation."
# )

# def rewrite_with_model(model, sql, instruction):
#     prompt = f"""
# You are an SQL REWRITER.

# Your ONLY task: output a rewritten SQL query.
# Do NOT output explanations, markdown, comments, or text.
# Do NOT repeat the instructions.
# Return ONLY the SQL query.

# STRICT RULES:
# {instruction}

# Original SQL:
# {sql}

# Rewritten SQL:
# """

#     try:
#         response = ollama.generate(
#             model=model,
#             prompt=prompt
#         )
#         print("Using model:", model)
#         sql = response["response"].strip()
#         sql = sql.replace("<s>", "").replace("</s>", "").strip()
#         return sql

#         # return response["response"].strip()
#     except Exception as e:
#         return f"ERROR: {str(e)}"


# def rewrite_sql_pipeline(sql):
#     rewritten = rewrite_with_model(PRIMARY_MODEL, sql, DEFAULT_INSTRUCTION)

#     if rewritten.startswith("ERROR") or not run_sql(rewritten)["success"]:
#         if FALLBACK_MODEL:
#             rewritten = rewrite_with_model(FALLBACK_MODEL, sql, DEFAULT_INSTRUCTION)

#     original_res = run_sql(sql)
#     rewritten_res = run_sql(rewritten)
#     comparison = compare_results(original_res, rewritten_res)

#     return {
#         "original": original_res,
#         "rewritten_sql": rewritten,
#         "rewritten_result": rewritten_res,
#         "comparison": comparison
#     }


from services.gemini_service import generate_sql_rewrite
from utils.sql_executor import run_sql
from utils.correctness import compare_results
from services.instruction_search import find_best_instruction


def rewrite_with_model(model: str, sql: str, instruction: str):
    """
    This wrapper keeps compatibility with instruction_search.
    It ignores 'model' and uses Gemini underneath.
    """
    try:
        return generate_sql_rewrite(sql, instruction)
    except Exception as e:
        return f"ERROR: {str(e)}"


def rewrite_sql_pipeline(sql: str):
    instruction_data = find_best_instruction("gemini", sql)
    instruction = instruction_data["instruction"]

    rewritten_sql = rewrite_with_model("gemini", sql, instruction)
    rewritten_sql = clean_sql(rewritten_sql)   # ← ADD THIS

    original_res = run_sql(sql)
    rewritten_res = run_sql(rewritten_sql)
    comparison = compare_results(original_res, rewritten_res)

    return {
        "original": original_res,
        "rewritten_sql": rewritten_sql,
        "rewritten_result": rewritten_res,
        "comparison": comparison
    }

def clean_sql(raw):
    if not raw:
        return raw
    return (
        raw.replace("```sql", "")
           .replace("```", "")
           .replace("<s>", "")
           .replace("</s>", "")
           .strip()
    )
