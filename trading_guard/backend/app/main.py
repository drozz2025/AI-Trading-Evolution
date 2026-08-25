from dataclasses import asdict
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .behaviour import detect_behaviour
from .demo import demo_account, demo_positions
from .mt5_provider import MetaApiProvider

app = FastAPI(title="Trading Guard API", version="0.3.0")

# Public demo is hosted on GitHub Pages. Production deployment should replace
# this wildcard with the exact application origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


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


@app.get("/api/v1/mt5/{account_id}/account")
async def mt5_account_endpoint(account_id: str) -> dict:
    """Read account state from MetaApi. No order execution is exposed."""
    try:
        account = await MetaApiProvider().get_account(account_id)
        return {"account": asdict(account)}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to read MT5 account") from exc


@app.get("/api/v1/mt5/{account_id}/positions")
async def mt5_positions_endpoint(account_id: str) -> dict:
    """Read open positions from MetaApi. No order execution is exposed."""
    try:
        positions = await MetaApiProvider().get_positions(account_id)
        return {"positions": positions}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to read MT5 positions") from exc
