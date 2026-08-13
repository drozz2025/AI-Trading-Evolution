"""Strategy research primitives for the multi-agent laboratory.

Agents do not receive a magic strategy. They produce explicit, testable hypotheses
with a causal idea, features, rules, risk limits, and an evaluation plan.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import hashlib
import json


@dataclass(frozen=True)
class StrategyHypothesis:
    name: str
    role: str
    thesis: str
    features: tuple[str, ...]
    entry_logic: str
    exit_logic: str
    risk_logic: str
    timeframe: str
    parameters: dict[str, float] = field(default_factory=dict)
    forbidden_shortcuts: tuple[str, ...] = ("RSI-only", "single-indicator crossover")

    @property
    def hypothesis_id(self) -> str:
        payload = {
            "name": self.name,
            "role": self.role,
            "thesis": self.thesis,
            "features": self.features,
            "entry": self.entry_logic,
            "exit": self.exit_logic,
            "risk": self.risk_logic,
            "timeframe": self.timeframe,
            "parameters": self.parameters,
        }
        raw = json.dumps(payload, sort_keys=True, default=str).encode()
        return hashlib.sha256(raw).hexdigest()[:12]


@dataclass
class ResearchResult:
    hypothesis_id: str
    train_score: float
    validation_score: float
    test_score: float | None
    max_drawdown: float
    trades: int
    status: str
    notes: list[str] = field(default_factory=list)

    @property
    def generalization_gap(self) -> float | None:
        if self.test_score is None:
            return None
        return self.validation_score - self.test_score


class ResearchGate:
    """Reject fragile research before it reaches the strategy arena."""

    def __init__(self, min_trades: int = 20, max_drawdown: float = 0.20, max_gap: float = 0.25):
        self.min_trades = min_trades
        self.max_drawdown = max_drawdown
        self.max_gap = max_gap

    def evaluate(self, result: ResearchResult) -> ResearchResult:
        notes = list(result.notes)
        if result.trades < self.min_trades:
            notes.append("insufficient_trade_count")
        if result.max_drawdown > self.max_drawdown:
            notes.append("drawdown_limit")
        if result.generalization_gap is not None and result.generalization_gap > self.max_gap:
            notes.append("generalization_gap")
        result.notes = notes
        result.status = "PROMOTE" if not notes and result.validation_score > 0 else "REJECT"
        return result
