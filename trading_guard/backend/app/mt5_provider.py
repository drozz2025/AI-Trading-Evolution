from dataclasses import dataclass
from typing import Protocol

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

class MetaApiProvider:
    """Adapter boundary for MetaApi. Credentials are never stored in this module.
    Production implementation is enabled only when METAAPI_TOKEN is configured.
    """
    def __init__(self, token: str | None = None):
        self.token = token

    async def get_account(self, external_id: str) -> MT5Account:
        raise NotImplementedError("MetaApi transport is intentionally disabled until credentials are configured")
