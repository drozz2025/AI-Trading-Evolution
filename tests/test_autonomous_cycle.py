from evolution.autonomous_cycle import Candidate, GatePolicy, ResearchCycle, Stage
from evolution.hypothesis_engine import Hypothesis


def candidate():
    return Candidate(Hypothesis(role="momentum", thesis="test thesis", features=("returns",), rules=("rule",)))


def test_cycle_promotes_survivor():
    result = ResearchCycle(GatePolicy(min_trades=5)).evaluate(
        candidate(),
        backtest=lambda h: {"score": 2.0, "trades": 10, "max_drawdown": 0.10},
        adversarial=lambda h: {"broken": False},
        validation=lambda h: {"score": 1.5, "test_score": 1.4},
    )
    assert result.stage is Stage.PROMOTED


def test_cycle_rejects_adversarial_failure():
    result = ResearchCycle().evaluate(
        candidate(),
        backtest=lambda h: {"score": 2.0, "trades": 30, "max_drawdown": 0.10},
        adversarial=lambda h: {"broken": True},
        validation=lambda h: {"score": 1.5, "test_score": 1.4},
    )
    assert result.stage is Stage.REJECTED
    assert result.reasons == ["adversarial_failure"]
