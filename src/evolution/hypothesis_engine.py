"""Autonomous research engine: agents generate and mutate explicit hypotheses."""
from __future__ import annotations

from dataclasses import dataclass, field
import random

from .research_roles import MANDATES, ResearchRole
from .strategy_lab import StrategyHypothesis


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str = "legacy"
    name: str = "unnamed"
    role: str = "unknown"
    thesis: str = ""
    features: tuple[str, ...] = ()
    entry_logic: str = ""
    exit_logic: str = ""
    risk_logic: str = ""
    timeframe: str = "1h"
    parameters: dict[str, float] = field(default_factory=dict)
    rules: tuple[str, ...] = ()
    forbidden_shortcuts: tuple[str, ...] = ("RSI-only", "single-indicator crossover")


@dataclass
class HypothesisArchive:
    seen: set[str] = field(default_factory=set)

    def add(self, hypothesis: StrategyHypothesis) -> bool:
        if hypothesis.hypothesis_id in self.seen:
            return False
        self.seen.add(hypothesis.hypothesis_id)
        return True


class HypothesisEngine:
    def __init__(self, seed: int = 42, archive: HypothesisArchive | None = None):
        self.rng = random.Random(seed)
        self.archive = archive or HypothesisArchive()
        self.counter = 0

    @staticmethod
    def _to_hypothesis(strategy: StrategyHypothesis) -> Hypothesis:
        return Hypothesis(
            hypothesis_id=strategy.hypothesis_id,
            name=strategy.name,
            role=strategy.role,
            thesis=strategy.thesis,
            features=strategy.features,
            entry_logic=strategy.entry_logic,
            exit_logic=strategy.exit_logic,
            risk_logic=strategy.risk_logic,
            timeframe=strategy.timeframe,
            parameters=dict(strategy.parameters),
            rules=(strategy.entry_logic, strategy.exit_logic, strategy.risk_logic),
            forbidden_shortcuts=strategy.forbidden_shortcuts,
        )

    def generate(self, agent_id: str, role: ResearchRole) -> Hypothesis:
        mandate = MANDATES[role]
        self.counter += 1
        feature_text = ", ".join(mandate.allowed_features)
        variants = [
            "condition on the current regime and test persistence",
            "compare behaviour before and after structural transitions",
            "test whether the effect survives volatility normalization",
            "test asymmetric exits while keeping entry logic stable",
        ]
        strategy = StrategyHypothesis(
            name=f"{role.value}-{agent_id}-H{self.counter:05d}",
            role=role.value,
            thesis=f"{mandate.objective}; {self.rng.choice(variants)}.",
            features=mandate.allowed_features,
            entry_logic=f"derive a rule from {feature_text} without future information",
            exit_logic="exit on thesis invalidation, time limit, or volatility-adjusted risk limit",
            risk_logic="position size capped; include spread, slippage and drawdown costs",
            timeframe=self.rng.choice(("5m", "15m", "1h", "4h")),
            parameters={"risk_fraction": round(self.rng.uniform(0.10, 0.50), 4)},
        )
        self.archive.add(strategy)
        return self._to_hypothesis(strategy)

    def mutate(self, parent: Hypothesis, agent_id: str) -> Hypothesis:
        self.counter += 1
        params = dict(parent.parameters)
        params["risk_fraction"] = round(max(0.05, min(0.75, params.get("risk_fraction", 0.25) * self.rng.uniform(0.8, 1.2))), 4)
        return Hypothesis(
            hypothesis_id=f"{parent.hypothesis_id}-M{self.counter:05d}",
            name=f"{parent.name}-{agent_id}-M{self.counter:05d}",
            role=parent.role,
            thesis=parent.thesis + " Child variant tests a controlled mutation.",
            features=parent.features,
            entry_logic=parent.entry_logic,
            exit_logic=parent.exit_logic,
            risk_logic=parent.risk_logic,
            timeframe=parent.timeframe,
            parameters=params,
            rules=parent.rules,
            forbidden_shortcuts=parent.forbidden_shortcuts,
        )
