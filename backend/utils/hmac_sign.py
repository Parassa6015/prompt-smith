import hmac
import hashlib
import json
import os

SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "super-secret-hmac-key")

def generate_signature(data):
    json_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
    signature = hmac.new(SECRET_KEY.encode(), json_data.encode(), hashlib.sha256).hexdigest()
    return signature


def verify_signature(data: dict, signature: str):
    expected = generate_signature(data)
    return hmac.compare_digest(expected, signature)
