from dataclasses import asdict
import asyncio
import json
import os
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .behaviour import detect_behaviour
from .demo import demo_account, demo_positions
from .mt5_provider import MetaApiProvider

app = FastAPI(title="Trading Guard API", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"] ,
)


class MT5ConnectRequest(BaseModel):
    login: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=1, max_length=128)
    server: str = Field(min_length=1, max_length=128)
    name: str = Field(default="Trading Guard account", min_length=1, max_length=100)
    platform: str = Field(default="mt5", pattern="^mt5$")
    read_only: bool = True


def _provision_account(payload: MT5ConnectRequest) -> dict:
    token = os.getenv("METAAPI_TOKEN")
    if not token:
        raise RuntimeError("METAAPI_TOKEN is not configured")

    body = {
        "login": payload.login,
        "password": payload.password,
        "name": payload.name,
        "server": payload.server,
        "platform": payload.platform,
        "magic": 0,
        "type": "cloud-g2",
        "manualTrades": False if payload.read_only else True,
    }
    request = Request(
        os.getenv(
            "METAAPI_PROVISIONING_URL",
            "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts",
        ),
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "auth-token": token,
            "transaction-id": os.urandom(16).hex(),
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "trading-guard-api"}


@app.get("/api/v1")
def api_root() -> dict[str, str]:
    return {"name": "Trading Guard", "mode": "read-only MVP"}


@app.get("/api/v1/demo/account")
def demo_account_endpoint() -> dict:
    account = demo_account()
    signals = detect_behaviour(
        account.trades_today,
        account.consecutive_losses,
        current_volume=0.20,
        previous_volume=0.10,
    )
    return {"account": asdict(account), "behaviour": [asdict(s) for s in signals]}


@app.get("/api/v1/demo/positions")
def demo_positions_endpoint() -> dict:
    return {"positions": [asdict(position) for position in demo_positions()]}


@app.post("/api/v1/mt5/connect")
async def connect_mt5_endpoint(payload: MT5ConnectRequest) -> dict:
    """Provision an MT5 account in MetaApi without storing the broker password."""
    try:
        result = await asyncio.to_thread(_provision_account, payload)
        account_id = result.get("id") or result.get("accountId")
        if not account_id:
            raise HTTPException(status_code=502, detail="MetaApi did not return an account id")
        return {
            "account_id": account_id,
            "state": result.get("state", "DEPLOYING"),
            "read_only": payload.read_only,
            "message": "MT5 account submitted to cloud. Connection may take a short time.",
        }
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to connect MT5 account") from exc


@app.get("/api/v1/mt5/{account_id}/account")
async def mt5_account_endpoint(account_id: str) -> dict:
    try:
        account = await MetaApiProvider().get_account(account_id)
        return {"account": asdict(account)}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to read MT5 account") from exc


@app.get("/api/v1/mt5/{account_id}/positions")
async def mt5_positions_endpoint(account_id: str) -> dict:
    try:
        positions = await MetaApiProvider().get_positions(account_id)
        return {"positions": positions}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to read MT5 positions") from exc
