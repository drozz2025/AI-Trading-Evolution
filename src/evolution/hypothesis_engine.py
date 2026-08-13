"""Autonomous research engine: agents generate and mutate explicit hypotheses."""
from __future__ import annotations

from dataclasses import dataclass, field
import random

from .research_roles import MANDATES, ResearchRole
from .strategy_lab import StrategyHypothesis


@dataclass(frozen=True)
class Hypothesis:
    """Compact hypothesis model used by the orchestration layer."""
    role: str
    thesis: str
    features: tuple[str, ...]
    rules: tuple[str, ...] = ()


@dataclass
class HypothesisArchive:
    seen: set[str] = field(default_factory=set)

    def add(self, hypothesis: StrategyHypothesis) -> bool:
        if hypothesis.hypothesis_id in self.seen:
            return False
        self.seen.add(hypothesis.hypothesis_id)
        return True


class HypothesisEngine:
    """Turns a research mandate into diverse, testable candidate hypotheses."""

    def __init__(self, seed: int = 42, archive: HypothesisArchive | None = None):
        self.rng = random.Random(seed)
        self.archive = archive or HypothesisArchive()
        self.counter = 0

    def generate(self, agent_id: str, role: ResearchRole) -> StrategyHypothesis:
        mandate = MANDATES[role]
        self.counter += 1
        feature_text = ", ".join(mandate.allowed_features)
        variants = [
            "condition on the current regime and test persistence",
            "compare behaviour before and after structural transitions",
            "test whether the effect survives volatility normalization",
            "test asymmetric exits while keeping entry logic stable",
        ]
        thesis = f"{mandate.objective}; {self.rng.choice(variants)}."
        hypothesis = StrategyHypothesis(
            name=f"{role.value}-{agent_id}-H{self.counter:05d}",
            role=role.value,
            thesis=thesis,
            features=mandate.allowed_features,
            entry_logic=f"derive a rule from {feature_text} without future information",
            exit_logic="exit on thesis invalidation, time limit, or volatility-adjusted risk limit",
            risk_logic="position size capped; include spread, slippage and drawdown costs",
            timeframe=self.rng.choice(("5m", "15m", "1h", "4h")),
            parameters={"risk_fraction": round(self.rng.uniform(0.10, 0.50), 4)},
        )
        self.archive.add(hypothesis)
        return hypothesis

    def mutate(self, parent: StrategyHypothesis, agent_id: str) -> StrategyHypothesis:
        """Create a child hypothesis with a controlled mutation."""
        self.counter += 1
        params = dict(parent.parameters)
        params["risk_fraction"] = round(
            max(0.05, min(0.75, params.get("risk_fraction", 0.25) * self.rng.uniform(0.8, 1.2))), 4
        )
        child = StrategyHypothesis(
            name=f"{parent.role}-{agent_id}-M{self.counter:05d}",
            role=parent.role,
            thesis=parent.thesis + " Child variant tests a controlled mutation.",
            features=parent.features,
            entry_logic=parent.entry_logic,
            exit_logic=parent.exit_logic,
            risk_logic=parent.risk_logic,
            timeframe=parent.timeframe,
            parameters=params,
            forbidden_shortcuts=parent.forbidden_shortcuts,
        )
        self.archive.add(child)
        return child
