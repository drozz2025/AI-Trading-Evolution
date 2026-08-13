from ai_trading_evolution.lab import ResearchLab


def main() -> None:
    lab = ResearchLab(min_validation_score=0.0, max_drawdown=0.25)
    candidates = [
        ("agent-001", "strategy-001", 1, 0.91, 0.72, 0.11),
        ("agent-002", "strategy-002", 1, 1.20, 0.31, 0.18),
        ("agent-003", "strategy-003", 1, 1.80, 0.95, 0.42),
    ]
    for candidate in candidates:
        result = lab.evaluate(*candidate)
        status = "ACCEPT" if result.accepted else "REJECT"
        print(f"{status} {result.agent_id} validation={result.validation_score:.3f} dd={result.max_drawdown:.3f}")


if __name__ == "__main__":
    main()
