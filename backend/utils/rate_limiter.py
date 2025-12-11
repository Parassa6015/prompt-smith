import time
from fastapi import HTTPException

# user_id → { count, reset_time }
RATE_STATE = {}

MAX_REQUESTS = 5         # allowed
WINDOW_SEC = 60          # per minute
CLEANUP_THRESHOLD = 1000 # Clean up when this many keys exist

def _cleanup_expired_entries(now: float):
    """Remove expired entries from RATE_STATE to prevent memory leak"""
    expired_keys = [
        key for key, data in RATE_STATE.items()
        if now >= data["reset"]
    ]
    for key in expired_keys:
        del RATE_STATE[key]

def rate_limit(user_id: int, endpoint="general"):
    now = time.time()
    key = f"{endpoint}:{user_id}"

    # Periodic cleanup to prevent memory leak
    if len(RATE_STATE) > CLEANUP_THRESHOLD:
        _cleanup_expired_entries(now)

    data = RATE_STATE.get(key)
    
    # If no data or window expired, reset
    if data is None or now >= data["reset"]:
        data = {
            "count": 0,
            "reset": now + WINDOW_SEC
        }
        RATE_STATE[key] = data  # ← ADD THIS LINE - save the reset data!
    
    print(f"[RATE LIMIT] User: {user_id}, Endpoint: {endpoint}, Count: {data['count']}/{MAX_REQUESTS}, Reset in: {int(data['reset'] - now)}s")
    
    # If too many requests → reject
    if data["count"] >= MAX_REQUESTS:
        remaining = int(data["reset"] - now)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {remaining} seconds."
        )
    
    # Allow & increment
    data["count"] += 1
    RATE_STATE[key] = data