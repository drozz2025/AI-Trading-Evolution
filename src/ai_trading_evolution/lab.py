from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Experiment:
    agent_id: str
    strategy_id: str
    revision: int
    train_score: float
    validation_score: float
    max_drawdown: float
    accepted: bool


class ResearchLab:
    """Small deterministic lab contract used before connecting market data."""

    def __init__(self, min_validation_score: float = 0.0, max_drawdown: float = 0.25):
        self.min_validation_score = min_validation_score
        self.max_drawdown = max_drawdown
        self.history: list[Experiment] = []

    def evaluate(self, agent_id: str, strategy_id: str, revision: int,
                 train_score: float, validation_score: float,
                 max_drawdown: float) -> Experiment:
        accepted = (
            validation_score >= self.min_validation_score
            and max_drawdown <= self.max_drawdown
        )
        result = Experiment(
            agent_id=agent_id,
            strategy_id=strategy_id,
            revision=revision,
            train_score=train_score,
            validation_score=validation_score,
            max_drawdown=max_drawdown,
            accepted=accepted,
        )
        self.history.append(result)
        return result

    def accepted(self) -> Iterable[Experiment]:
        return (x for x in self.history if x.accepted)

    def snapshot(self) -> list[dict]:
        return [asdict(x) for x in self.history]
