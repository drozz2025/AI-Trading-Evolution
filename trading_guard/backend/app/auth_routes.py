from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr, Field
from .auth import register, login, logout, user_id_from_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

@router.post("/register")
def register_route(payload: Credentials):
    try: user_id = register(payload.email, payload.password)
    except ValueError as exc: raise HTTPException(409, str(exc)) from exc
    return {"user_id": user_id, "message": "Account created"}

@router.post("/login")
def login_route(payload: Credentials):
    try: token = login(payload.email, payload.password)
    except ValueError as exc: raise HTTPException(401, "Invalid credentials") from exc
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout_route(authorization: str | None = Header(default=None)):
    token = authorization.removeprefix("Bearer ").strip() if authorization else ""
    if token: logout(token)
    return {"ok": True}

@router.get("/me")
def me(authorization: str | None = Header(default=None)):
    token = authorization.removeprefix("Bearer ").strip() if authorization else ""
    uid = user_id_from_token(token)
    if not uid: raise HTTPException(401, "Authentication required")
    return {"user_id": uid}
