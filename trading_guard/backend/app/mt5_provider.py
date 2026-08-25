from dataclasses import dataclass
from typing import Protocol
import os
from urllib.request import Request, urlopen
import json
import asyncio

@dataclass(frozen=True)
class MT5Account:
    external_id: str
    broker: str
    server: str
    balance: float
    equity: float
    currency: str

class MT5Provider(Protocol):
    async def get_account(self, external_id: str) -> MT5Account: ...
    async def get_positions(self, external_id: str) -> list[dict]: ...

class MetaApiProvider:
    """Read-only MetaApi adapter for cloud MT5 monitoring.

    METAAPI_TOKEN stays server-side. The browser never receives this token.
    """
    def __init__(self, token: str | None = None, base_url: str | None = None):
        self.token = token or os.getenv("METAAPI_TOKEN")
        self.base_url = (base_url or os.getenv(
            "METAAPI_CLIENT_BASE_URL",
            "https://mt-client-api-v1.new-york.agiliumtrade.ai",
        )).rstrip("/")

    def _get(self, path: str):
        if not self.token:
            raise RuntimeError("METAAPI_TOKEN is not configured")
        req = Request(
            f"{self.base_url}{path}",
            headers={"Accept": "application/json", "auth-token": self.token},
            method="GET",
        )
        with urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))

    async def get_account(self, external_id: str) -> MT5Account:
        data = await asyncio.to_thread(
            self._get, f"/users/current/accounts/{external_id}/account-information"
        )
        return MT5Account(
            external_id=external_id,
            broker=data.get("broker", ""),
            server=data.get("server", ""),
            balance=float(data.get("balance", 0)),
            equity=float(data.get("equity", 0)),
            currency=data.get("currency", "USD"),
        )

    async def get_positions(self, external_id: str) -> list[dict]:
        return await asyncio.to_thread(
            self._get, f"/users/current/accounts/{external_id}/positions"
        )
