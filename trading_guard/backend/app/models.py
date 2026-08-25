from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class AccountSnapshot:
    account_id: str
    balance: float
    equity: float
    daily_pnl: float
    trades_today: int
    consecutive_losses: int
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
class TradeEvent:
    trade_id: str
    symbol: str
    side: str
    volume: float
    profit: float
    opened_at: datetime
    closed_at: datetime | None = None
