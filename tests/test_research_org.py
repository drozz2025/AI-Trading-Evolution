from evolution.agent_org import ResearchDirector
from evolution.orchestrator import ResearchOrchestrator
from evolution.strategy_lab import ResearchGate, ResearchResult


def test_director_seeds_diverse_roles():
    director = ResearchDirector()
    director.seed(12)
    assert len(director.agents) == 12
    assert len({a.role for a in director.agents}) >= 8


def test_gate_rejects_fragile_result():
    result = ResearchResult(
        hypothesis_id="x",
        train_score=3.0,
        validation_score=1.0,
        test_score=0.2,
        max_drawdown=0.10,
        trades=10,
        status="PENDING",
    )
    evaluated = ResearchGate(min_trades=20).evaluate(result)
    assert evaluated.status == "REJECT"


def test_orchestrator_promotes_robust_result():
    org = ResearchOrchestrator()
    org.bootstrap(12)
    result = ResearchResult(
        hypothesis_id="robust",
        train_score=1.4,
        validation_score=1.1,
        test_score=1.0,
        max_drawdown=0.08,
        trades=100,
        status="PENDING",
    )
    evaluated = org.submit(result, "R-0001")
    assert evaluated.status == "PROMOTE"
    assert org.snapshot()["arena_size"] == 1
