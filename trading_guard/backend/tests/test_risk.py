from app.risk import RiskConfig, evaluate_account

def test_daily_loss_warning():
    warnings = evaluate_account(10_000, 9_700, -210, 1, 0)
    assert "daily_loss_limit" in warnings

def test_consecutive_loss_warning():
    warnings = evaluate_account(10_000, 10_000, 0, 2, 2, RiskConfig(max_consecutive_losses=2))
    assert "consecutive_loss_limit" in warnings

def test_trade_count_warning():
    warnings = evaluate_account(10_000, 10_000, 0, 5, 0)
    assert "trade_count_limit" in warnings
