from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# 32-byte key for AES-256
AES_KEY = os.environ.get("AES_SECRET_KEY")

if AES_KEY is None:
    raise Exception("AES_SECRET_KEY not set in environment")

AES_KEY = AES_KEY.encode()  # convert to bytes
BLOCK_SIZE = AES.block_size  # 16 bytes


def pad(data: bytes):
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding]) * padding


def unpad(data: bytes):
    padding = data[-1]
    return data[:-padding]


def encrypt_text(text: str) -> str:
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode()))
    return base64.b64encode(cipher.iv + ct_bytes).decode()


def decrypt_text(encoded: str) -> str:
    raw = base64.b64decode(encoded)
    iv = raw[:BLOCK_SIZE]
    ct = raw[BLOCK_SIZE:]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ct)).decode()
