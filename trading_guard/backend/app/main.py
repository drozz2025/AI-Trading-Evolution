from dataclasses import asdict
from fastapi import FastAPI

from .behaviour import detect_behaviour
from .demo import demo_account, demo_positions

app = FastAPI(title="Trading Guard API", version="0.2.0")


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
