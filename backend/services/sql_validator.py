import re
from fastapi import HTTPException

# Dangerous SQL patterns that should NEVER be allowed
BLOCKED_PATTERNS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bTRUNCATE\b",
    r"\bALTER\b",
    r"\bUPDATE\b",
    r"\bINSERT\b",
    r"\bMERGE\b",
    r"\bCREATE\b",      # prevent schema modifications
    r";\s*--",          # comment injection
    r"--\s*$",          # comment at end of query
    r";.*;",            # multi-statement chains
    r"\bEXEC\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bCALL\b",
]

# Allowed SELECT-only structure
SELECT_ONLY_PATTERN = r"^\s*SELECT\b"


def validate_sql(sql: str):
    """Validate SQL for safety before execution."""
    cleaned = sql.strip().upper()

    # 1. Must start with SELECT
    if not re.match(SELECT_ONLY_PATTERN, cleaned, re.IGNORECASE):
        raise HTTPException(
            status_code=400,
            detail="Only SELECT queries are allowed for safety."
        )

    # 2. Block dangerous commands
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise HTTPException(
                status_code=400,
                detail=f"Query contains blocked pattern: {pattern}"
            )

    # 3. Prevent multiple statements
    if cleaned.count(";") > 1:
        raise HTTPException(
            status_code=400,
            detail="Multiple SQL statements are not allowed."
        )

    # 4. Prevent infinite recursive CTE without limit
    if "WITH RECURSIVE" in cleaned and "LIMIT" not in cleaned:
        raise HTTPException(
            status_code=400,
            detail="Recursive CTEs must include a LIMIT clause."
        )

    # 5. No writing keywords anywhere
    write_ops = ["UPDATE ", "DELETE ", "INSERT ", "CREATE ", "DROP "]
    for op in write_ops:
        if op in cleaned:
            raise HTTPException(
                status_code=400,
                detail=f"Write operation '{op.strip()}' is not allowed."
            )

    return True

def is_sql_safe(sql: str):
    s = sql.lower()

    forbidden = [
        r"\bdelete\b", r"\bdrop\b", r"\btruncate\b",
        r"\binsert\b", r"\bupdate\b"
    ]

    for pattern in forbidden:
        if re.search(pattern, s):
            return False

    return True

