from ai_trading_evolution.lab import ResearchLab


def test_good_candidate_is_accepted():
    lab = ResearchLab(min_validation_score=0.0, max_drawdown=0.25)
    result = lab.evaluate("agent-001", "strategy-001", 1, 1.2, 0.8, 0.12)
    assert result.accepted is True


def test_excessive_drawdown_is_rejected():
    lab = ResearchLab(min_validation_score=0.0, max_drawdown=0.25)
    result = lab.evaluate("agent-002", "strategy-002", 1, 2.0, 1.0, 0.40)
    assert result.accepted is False
