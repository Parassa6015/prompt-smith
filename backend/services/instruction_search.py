# from utils.sql_executor import run_sql
# from utils.correctness import compare_results

# INSTRUCTIONS = [
#     "Rewrite the SQL to improve performance. Preserve all column aliases.",
#     "Rewrite the SQL for readability. Do not change column names.",
#     "Rewrite the SQL minimizing subqueries. Preserve results.",
#     "Optimize joins and filtering. Output only the rewritten SQL.",
#     "Standardize formatting and spacing. Do NOT modify logic.",
#     "Rewrite the SQL using index-friendly operations. Keep output identical.",
#     "Rewrite for ANSI SQL compliance. Preserve aliases.",
#     "Rewrite the SQL with strict alias preservation and no aggregate simplification."
# ]


# def clean_sql(text: str) -> str:
#     """Remove markdown, tags, and junk tokens that break SQL execution."""
#     if not text:
#         return ""

#     bad_prefixes = ["```", "```sql", "<s>", "</s>", "Optimized Query:", "Efficient Query:", "\"\"\"", "EOF:"]
#     clean = text.strip()

#     for bad in bad_prefixes:
#         clean = clean.replace(bad, "")

#     # Remove trailing semicolons duplicates
#     clean = clean.replace(";;", ";")

#     return clean.strip()


# def test_instruction(model, sql, instruction):
#     try:
#         raw_rewritten = rewrite_with_model(model, sql, instruction)
#         rewritten = clean_sql(raw_rewritten)

#         rewritten_res = run_sql(rewritten)
#         original_res = run_sql(sql)

#         comparison = compare_results(original_res, rewritten_res)

#         score = 0
#         if rewritten_res["success"]:
#             score += 1
#         if comparison["valid"]:
#             score += 2

#         return {
#             "instruction": instruction,
#             "rewritten_sql": rewritten,
#             "result": rewritten_res,
#             "comparison": comparison,
#             "score": score
#         }
#     except Exception as e:
#         return {
#             "instruction": instruction,
#             "rewritten_sql": "",
#             "result": {"success": False, "error": str(e)},
#             "comparison": {"valid": False, "reason": "exception"},
#             "score": 0
#         }


# def find_best_instruction(model, sql):
#     results = [test_instruction(model, sql, inst) for inst in INSTRUCTIONS]
#     best = max(results, key=lambda x: x["score"])
#     return {
#         "best_instruction": best,
#         "all_results": results
#     }
# def find_best_instruction(model: str, query: str):
#     return {
#         "instruction": "Rewrite SQL without changing meaning.",
#         "reason": "Instruction search disabled."
#     }


"""
Lightweight instruction selector.
You can expand this later, but this avoids import errors.
"""

def find_best_instruction(model: str, query: str):
    return {
        "instruction": (
            "Optimize this SQL query for performance while maintaining exact same results.\n\n"
            "Allowed optimizations:\n"
            "✅ Remove unnecessary subqueries\n"
            "✅ Optimize JOIN order (smaller tables first)\n"
            "✅ Convert NOT IN to NOT EXISTS or LEFT JOIN\n"
            "✅ Push down WHERE filters before JOINs\n"
            "✅ Remove redundant DISTINCT/GROUP BY\n"
            "✅ Use indexes hints if beneficial\n"
            "✅ Simplify complex CASE statements\n"
            "✅ Better formatting & readability\n\n"
            "DO NOT change:\n"
            "❌ Column names or aliases\n"
            "❌ Business logic or filters\n"
            "❌ Final result set\n\n"
            "Output ONLY optimized SQL, no explanation."
        ),
        "reason": "Performance optimization"
    }