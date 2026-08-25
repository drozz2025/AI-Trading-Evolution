from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class AccountSnapshot:
    account_id: str
    balance: float
    equity: float
    margin: float
    free_margin: float
    captured_at: datetime

@dataclass(frozen=True)
class PositionSnapshot:
    position_id: str
    symbol: str
    side: str
    volume: float
    entry_price: float
    stop_loss: float | None
    take_profit: float | None
    profit: float

@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    risk_percent: float
    reason: str
