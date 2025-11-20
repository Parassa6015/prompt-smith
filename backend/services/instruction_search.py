from services.llm_service import rewrite_with_model
from utils.sql_executor import run_sql
from utils.correctness import compare_results

INSTRUCTIONS = [
    "Rewrite the SQL to improve performance. Preserve all column aliases.",
    "Rewrite the SQL for readability. Do not change column names.",
    "Rewrite the SQL minimizing subqueries. Preserve results.",
    "Optimize joins and filtering. Output only the rewritten SQL.",
    "Standardize formatting and spacing. Do NOT modify logic.",
    "Rewrite the SQL using index-friendly operations. Keep output identical.",
    "Rewrite for ANSI SQL compliance. Preserve aliases.",
    "Rewrite the SQL with strict alias preservation and no aggregate simplification."
]

def test_instruction(model, sql, instruction):
    rewritten = rewrite_with_model(model, sql, instruction)
    rewritten_res = run_sql(rewritten)
    comparison = compare_results(run_sql(sql), rewritten_res)

    score = 0
    if rewritten_res["success"]:
        score += 1
    if comparison["valid"]:
        score += 2

    return {
        "instruction": instruction,
        "rewritten_sql": rewritten,
        "result": rewritten_res,
        "comparison": comparison,
        "score": score
    }


def find_best_instruction(model, sql):
    results = []
    for inst in INSTRUCTIONS:
        r = test_instruction(model, sql, inst)
        results.append(r)

    # pick instruction with highest score
    best = max(results, key=lambda x: x["score"])
    
    return {
        "best_instruction": best,
        "all_results": results
    }
