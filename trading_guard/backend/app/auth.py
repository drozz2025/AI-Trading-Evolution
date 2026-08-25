import hashlib,hmac,os,secrets,sqlite3,time
from pathlib import Path
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .audit import log
DB_PATH=Path(os.getenv("AUTH_DB_PATH","/tmp/trading_guard_auth.sqlite3")); SESSION_TTL=int(os.getenv("SESSION_TTL_SECONDS","86400"))
def _db():
 c=sqlite3.connect(DB_PATH); c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at INTEGER NOT NULL)"); c.execute("CREATE TABLE IF NOT EXISTS sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL, expires_at INTEGER NOT NULL)"); c.commit(); return c
def _hash_password(password,salt=None):
 salt=salt or secrets.token_bytes(16); return salt.hex()+":"+hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1).hex()
def _verify_password(password,stored):
 salt_hex,digest_hex=stored.split(":",1); return hmac.compare_digest(hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt_hex),n=2**14,r=8,p=1).hex(),digest_hex)
def register(email,password):
 email=email.strip().lower()
 if len(password)<8: raise ValueError("Password must contain at least 8 characters")
 c=_db()
 try: cur=c.execute("INSERT INTO users(email,password_hash,created_at) VALUES(?,?,?)",(email,_hash_password(password),int(time.time()))); c.commit(); uid=int(cur.lastrowid); log(uid,"REGISTER"); return uid
 except sqlite3.IntegrityError as e: raise ValueError("Email already registered") from e
 finally: c.close()
def login(email,password):
 c=_db(); row=c.execute("SELECT id,password_hash FROM users WHERE email=?",(email.strip().lower(),)).fetchone()
 if not row or not _verify_password(password,row[1]): c.close(); raise ValueError("Invalid credentials")
 token=secrets.token_urlsafe(32); c.execute("INSERT INTO sessions(token_hash,user_id,expires_at) VALUES(?,?,?)",(hashlib.sha256(token.encode()).hexdigest(),row[0],int(time.time())+SESSION_TTL)); c.commit(); c.close(); log(row[0],"LOGIN"); return token
def google_login(credential):
 client_id=os.getenv("GOOGLE_CLIENT_ID")
 if not client_id: raise RuntimeError("GOOGLE_CLIENT_ID is not configured")
 try: info=id_token.verify_oauth2_token(credential,google_requests.Request(),client_id)
 except Exception as e: raise ValueError("Invalid Google credential") from e
 email=str(info.get("email","")).strip().lower()
 if not email or not info.get("email_verified"): raise ValueError("Google email is not verified")
 c=_db(); row=c.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone()
 if row: uid=int(row[0])
 else:
  # Google-only accounts receive a random unusable password hash; sign-in is handled by Google.
  cur=c.execute("INSERT INTO users(email,password_hash,created_at) VALUES(?,?,?)",(email,_hash_password(secrets.token_urlsafe(32)),int(time.time()))); c.commit(); uid=int(cur.lastrowid); log(uid,"REGISTER_GOOGLE")
 token=secrets.token_urlsafe(32); c.execute("INSERT INTO sessions(token_hash,user_id,expires_at) VALUES(?,?,?)",(hashlib.sha256(token.encode()).hexdigest(),uid,int(time.time())+SESSION_TTL)); c.commit(); c.close(); log(uid,"LOGIN_GOOGLE"); return token
def user_id_from_token(token):
 if not token:return None
 c=_db(); row=c.execute("SELECT user_id FROM sessions WHERE token_hash=? AND expires_at>?",(hashlib.sha256(token.encode()).hexdigest(),int(time.time()))).fetchone(); c.close(); return int(row[0]) if row else None
def logout(token):
 uid=user_id_from_token(token); c=_db(); c.execute("DELETE FROM sessions WHERE token_hash=?",(hashlib.sha256(token.encode()).hexdigest(),)); c.commit(); c.close()
 if uid: log(uid,"LOGOUT")
