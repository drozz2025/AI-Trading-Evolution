from dataclasses import asdict
import asyncio
import json
import os
from urllib.request import Request, urlopen
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .auth import user_id_from_token
from .auth_routes import router as auth_router
from .admin import router as admin_router
from .behaviour import detect_behaviour
from .demo import demo_account, demo_positions
from .mt5_provider import MetaApiProvider
from .risk_engine import assess
app = FastAPI(title="Trading Guard API", version="0.7.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(auth_router); app.include_router(admin_router)
def require_user(authorization: str | None) -> int:
    token = authorization.removeprefix("Bearer ").strip() if authorization else ""; uid = user_id_from_token(token)
    if not uid: raise HTTPException(401, "Authentication required")
    return uid
class MT5ConnectRequest(BaseModel):
    login: str = Field(min_length=1, max_length=32); password: str = Field(min_length=1, max_length=128); server: str = Field(min_length=1, max_length=128); name: str = Field(default="Trading Guard account", min_length=1, max_length=100); platform: str = Field(default="mt5", pattern="^mt5$"); read_only: bool = True
def _provision_account(payload: MT5ConnectRequest) -> dict:
    token = os.getenv("METAAPI_TOKEN")
    if not token: raise RuntimeError("METAAPI_TOKEN is not configured")
    body = {"login":payload.login,"password":payload.password,"name":payload.name,"server":payload.server,"platform":payload.platform,"magic":0,"type":"cloud-g2","manualTrades":False}
    request = Request(os.getenv("METAAPI_PROVISIONING_URL", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts"), data=json.dumps(body).encode(), headers={"Accept":"application/json","Content-Type":"application/json","auth-token":token,"transaction-id":os.urandom(16).hex()}, method="POST")
    with urlopen(request, timeout=30) as response: return json.loads(response.read().decode())
@app.get("/health")
def health(): return {"status":"ok","service":"trading-guard-api"}
@app.get("/api/v1")
def api_root(): return {"name":"Trading Guard","mode":"read-only MVP"}
@app.get("/api/v1/demo/account")
def demo_account_endpoint(authorization: str | None = Header(default=None)):
    require_user(authorization); account=demo_account(); signals=detect_behaviour(account.trades_today,account.consecutive_losses,current_volume=.20,previous_volume=.10); risk=assess(consecutive_losses=account.consecutive_losses,trades_today=account.trades_today,current_volume=.20,previous_volume=.10); return {"account":asdict(account),"behaviour":[asdict(s) for s in signals],"risk":asdict(risk)}
@app.get("/api/v1/demo/positions")
def demo_positions_endpoint(authorization: str | None = Header(default=None)): require_user(authorization); return {"positions":[asdict(p) for p in demo_positions()]}
@app.post("/api/v1/mt5/connect")
async def connect_mt5_endpoint(payload: MT5ConnectRequest, authorization: str | None = Header(default=None)):
    user_id=require_user(authorization)
    try:
        result=await asyncio.to_thread(_provision_account,payload); account_id=result.get("id") or result.get("accountId")
        if not account_id: raise HTTPException(502,"MetaApi did not return an account id")
        return {"user_id":user_id,"account_id":account_id,"state":result.get("state","DEPLOYING"),"read_only":True,"message":"MT5 account submitted to cloud."}
    except HTTPException: raise
    except RuntimeError as exc: raise HTTPException(503,str(exc)) from exc
    except Exception as exc: raise HTTPException(502,"Unable to connect MT5 account") from exc
@app.get("/api/v1/mt5/{account_id}/account")
async def mt5_account_endpoint(account_id:str,authorization:str|None=Header(default=None)):
    require_user(authorization)
    try:return {"account":asdict(await MetaApiProvider().get_account(account_id))}
    except RuntimeError as exc:raise HTTPException(503,str(exc)) from exc
    except Exception as exc:raise HTTPException(502,"Unable to read MT5 account") from exc
@app.get("/api/v1/mt5/{account_id}/positions")
async def mt5_positions_endpoint(account_id:str,authorization:str|None=Header(default=None)):
    require_user(authorization)
    try:return {"positions":await MetaApiProvider().get_positions(account_id)}
    except RuntimeError as exc:raise HTTPException(503,str(exc)) from exc
    except Exception as exc:raise HTTPException(502,"Unable to read MT5 positions") from exc
@app.post("/api/v1/risk/assess")
def risk_assess(consecutive_losses:int=0,trades_today:int=0,current_volume:float=0,previous_volume:float=0,floating_loss_pct:float=0,authorization:str|None=Header(default=None)):
    require_user(authorization); return {"risk":asdict(assess(consecutive_losses=consecutive_losses,trades_today=trades_today,current_volume=current_volume,previous_volume=previous_volume,floating_loss_pct=floating_loss_pct))}
