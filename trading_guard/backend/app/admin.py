import os
import sqlite3
import time
from fastapi import APIRouter, Header, HTTPException
from .auth import user_id_from_token, _db

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
ADMIN_EMAILS = {x.strip().lower() for x in os.getenv("ADMIN_EMAILS", "").split(",") if x.strip()}

def require_admin(authorization: str | None):
    token = authorization.removeprefix("Bearer ").strip() if authorization else ""
    uid = user_id_from_token(token)
    if not uid: raise HTTPException(401, "Authentication required")
    conn = _db(); row = conn.execute("SELECT email FROM users WHERE id=?", (uid,)).fetchone(); conn.close()
    if not row or row[0].lower() not in ADMIN_EMAILS: raise HTTPException(403, "Admin access required")
    return uid

@router.get("/overview")
def overview(authorization: str | None = Header(default=None)):
    require_admin(authorization)
    conn = _db()
    users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    sessions = conn.execute("SELECT COUNT(*) FROM sessions WHERE expires_at > strftime('%s','now')").fetchone()[0]
    conn.close()
    return {"users": users, "active_sessions": sessions, "mode": "read-only", "trading_execution": "disabled", "server_time": int(time.time())}

@router.get("/users")
def users(authorization: str | None = Header(default=None)):
    require_admin(authorization)
    conn = _db(); rows = conn.execute("SELECT id,email,created_at FROM users ORDER BY id DESC").fetchall(); conn.close()
    return {"users":[{"id":r[0],"email":r[1],"created_at":r[2]} for r in rows]}

@router.get("/security")
def security(authorization: str | None = Header(default=None)):
    require_admin(authorization)
    conn = _db(); expired = conn.execute("SELECT COUNT(*) FROM sessions WHERE expires_at <= strftime('%s','now')").fetchone()[0]; conn.close()
    return {"authentication":"enabled", "session_expiry":True, "expired_sessions":expired, "trading_execution":"disabled", "admin_allowlist_configured":bool(ADMIN_EMAILS)}
