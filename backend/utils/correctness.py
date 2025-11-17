from utils.sql_executor import run_sql

def compare_results(original, rewritten):
    """
    Compare two SQL execution results.
    Each input is the dict returned by run_sql().
    Returns:
    - valid: bool
    - reason: string
    """

    if not original["success"]:
        return {"valid": False, "reason": "Original SQL failed"}

    if not rewritten["success"]:
        return {"valid": False, "reason": f"Rewrite failed: {rewritten['error']}"}

    # Compare columns
    if original["columns"] != rewritten["columns"]:
        return {"valid": False, "reason": "Column mismatch"}

    # Compare row count
    if len(original["rows"]) != len(rewritten["rows"]):
        return {"valid": False, "reason": "Row count mismatch"}

    # Compare row-by-row values
    for r1, r2 in zip(original["rows"], rewritten["rows"]):
        if r1 != r2:
            return {"valid": False, "reason": "Row value mismatch"}

    return {"valid": True, "reason": "Results match"}
