"""Run one complete autonomous research cycle in simulation only."""
from evolution.hypothesis_engine import HypothesisEngine
from evolution.autonomous_cycle import Candidate, ResearchCycle
from evolution.research_roles import ResearchRole


def main() -> None:
    engine = HypothesisEngine(seed=11)
    roles = list(ResearchRole)[:8]
    candidates = [Candidate(engine.generate(f"AGENT-{i+1:04d}", role)) for i, role in enumerate(roles)]

    def backtest(h):
        return {"trades": 40, "return_pct": 8.0, "drawdown_pct": 3.0, "sharpe": 1.7}

    def adversarial(h, result):
        return {"passed": True, "reason": "No synthetic adversarial failure triggered."}

    def validation(h, result):
        return {"passed": True, "return_pct": 5.0, "drawdown_pct": 3.5, "sharpe": 1.3}

    results = ResearchCycle().run(
        candidates,
        backtest=backtest,
        adversarial=adversarial,
        validation=validation,
    )
    promoted = [r for r in results if r.stage.value == "promoted"]
    print("END-TO-END LAB OK")
    print({"generated": len(results), "promoted": len(promoted), "rejected": len(results) - len(promoted)})
    print("promoted:", [r.hypothesis.name for r in promoted])


if __name__ == "__main__":
    main()
