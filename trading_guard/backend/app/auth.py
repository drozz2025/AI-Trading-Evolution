import hashlib
import hmac
import os
import secrets
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(os.getenv("AUTH_DB_PATH", "/tmp/trading_guard_auth.sqlite3"))
SESSION_TTL = int(os.getenv("SESSION_TTL_SECONDS", "86400"))


def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at INTEGER NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL, expires_at INTEGER NOT NULL)")
    conn.commit()
    return conn


def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + ":" + digest.hex()


def _verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split(":", 1)
    expected = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(expected.hex(), digest_hex)


def register(email: str, password: str) -> int:
    email = email.strip().lower()
    if len(password) < 8: raise ValueError("Password must contain at least 8 characters")
    conn = _db()
    try:
        cur = conn.execute("INSERT INTO users(email,password_hash,created_at) VALUES(?,?,?)", (email, _hash_password(password), int(time.time())))
        conn.commit()
        return int(cur.lastrowid)
    except sqlite3.IntegrityError as exc:
        raise ValueError("Email already registered") from exc
    finally: conn.close()


def login(email: str, password: str) -> str:
    conn = _db()
    row = conn.execute("SELECT id,password_hash FROM users WHERE email=?", (email.strip().lower(),)).fetchone()
    if not row or not _verify_password(password, row[1]):
        conn.close(); raise ValueError("Invalid credentials")
    token = secrets.token_urlsafe(32)
    conn.execute("INSERT INTO sessions(token_hash,user_id,expires_at) VALUES(?,?,?)", (hashlib.sha256(token.encode()).hexdigest(), row[0], int(time.time()) + SESSION_TTL))
    conn.commit(); conn.close()
    return token


def user_id_from_token(token: str) -> int | None:
    if not token: return None
    conn = _db()
    row = conn.execute("SELECT user_id FROM sessions WHERE token_hash=? AND expires_at>?", (hashlib.sha256(token.encode()).hexdigest(), int(time.time()))).fetchone()
    conn.close()
    return int(row[0]) if row else None


def logout(token: str) -> None:
    conn = _db(); conn.execute("DELETE FROM sessions WHERE token_hash=?", (hashlib.sha256(token.encode()).hexdigest(),)); conn.commit(); conn.close()
