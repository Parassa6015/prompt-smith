from utils.sql_executor import run_sql

def normalize_row(row):
    """
    Convert row keys to lowercase and sort items so column order differences don't matter.
    But keep values exactly the same.
    """
    return {k.lower(): v for k, v in row.items()}


def compare_results(original, rewritten):
    # If either query failed → invalid
    if not original["success"]:
        return {"valid": False, "reason": "Original SQL failed"}
    if not rewritten["success"]:
        return {"valid": False, "reason": "Rewritten SQL failed"}

    # Number of rows must match
    if len(original["rows"]) != len(rewritten["rows"]):
        return {"valid": False, "reason": "Row count mismatch"}

    # Normalize rows to ignore alias differences
    original_norm = [normalize_row(r) for r in original["rows"]]
    rewritten_norm = [normalize_row(r) for r in rewritten["rows"]]

    # Compare each row's values
    for o_row, r_row in zip(original_norm, rewritten_norm):
        if o_row != r_row:
            return {"valid": False, "reason": "Row value mismatch"}

    return {"valid": True, "reason": "Results match (alias differences ignored)"}
