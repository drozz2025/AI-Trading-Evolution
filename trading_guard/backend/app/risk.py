from dataclasses import dataclass

@dataclass(frozen=True)
class RiskConfig:
    max_risk_percent: float = 0.5
    max_daily_loss_percent: float = 2.0
    max_consecutive_losses: int = 2
    max_trades_per_day: int = 5

def evaluate_account(balance: float, equity: float, daily_pnl: float, trades_today: int, consecutive_losses: int, config: RiskConfig = RiskConfig()) -> list[str]:
    warnings: list[str] = []
    if balance <= 0:
        warnings.append("invalid_balance")
        return warnings
    drawdown_percent = max(0.0, (balance - equity) / balance * 100)
    daily_loss_percent = max(0.0, -daily_pnl / balance * 100)
    if daily_loss_percent >= config.max_daily_loss_percent:
        warnings.append("daily_loss_limit")
    if trades_today >= config.max_trades_per_day:
        warnings.append("trade_count_limit")
    if consecutive_losses >= config.max_consecutive_losses:
        warnings.append("consecutive_loss_limit")
    if drawdown_percent >= config.max_daily_loss_percent:
        warnings.append("drawdown_limit")
    return warnings
