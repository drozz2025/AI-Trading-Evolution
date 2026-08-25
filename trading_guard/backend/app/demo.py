from datetime import datetime, timezone
from .models import AccountSnapshot, PositionSnapshot


def demo_account() -> AccountSnapshot:
    return AccountSnapshot(
        account_id="demo-001",
        balance=10_000.0,
        equity=9_870.0,
        daily_pnl=-130.0,
        trades_today=4,
        consecutive_losses=2,
        captured_at=datetime.now(timezone.utc),
    )


def demo_positions() -> list[PositionSnapshot]:
    return [
        PositionSnapshot(
            position_id="demo-pos-001",
            symbol="XAUUSD",
            side="BUY",
            volume=0.20,
            entry_price=3385.20,
            stop_loss=3380.20,
            take_profit=3395.20,
            profit=-42.0,
        )
    ]
