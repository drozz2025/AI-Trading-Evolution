"""Deterministic orchestration skeleton for autonomous strategy research.

This module deliberately contains no broker connectivity and no live execution.
It coordinates hypothesis generation, evaluation, adversarial review, and promotion
as a laboratory workflow.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable

from .hypothesis_engine import Hypothesis


class Stage(str, Enum):
    RESEARCH = "research"
    BACKTEST = "backtest"
    ADVERSARIAL = "adversarial"
    VALIDATION = "validation"
    PROMOTED = "promoted"
    REJECTED = "rejected"


@dataclass
class Candidate:
    hypothesis: Hypothesis
    stage: Stage = Stage.RESEARCH
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GatePolicy:
    min_trades: int = 20
    max_drawdown: float = 0.20
    min_test_score: float = 0.0
    max_validation_test_gap: float = 0.50


@dataclass
class ResearchCycle:
    policy: GatePolicy = field(default_factory=GatePolicy)

    def evaluate(
        self,
        candidate: Candidate,
        *,
        backtest: Callable[[Hypothesis], dict[str, float]],
        adversarial: Callable[[Hypothesis], dict[str, float]],
        validation: Callable[[Hypothesis], dict[str, float]],
    ) -> Candidate:
        bt = backtest(candidate.hypothesis)
        candidate.score = float(bt.get("score", 0.0))
        if int(bt.get("trades", 0)) < self.policy.min_trades:
            return self._reject(candidate, "insufficient_trades")
        if float(bt.get("max_drawdown", 1.0)) > self.policy.max_drawdown:
            return self._reject(candidate, "backtest_drawdown")
        candidate.stage = Stage.ADVERSARIAL

        attack = adversarial(candidate.hypothesis)
        if bool(attack.get("broken", False)):
            return self._reject(candidate, "adversarial_failure")
        candidate.stage = Stage.VALIDATION

        val = validation(candidate.hypothesis)
        val_score = float(val.get("score", 0.0))
        test_score = float(val.get("test_score", val_score))
        gap = abs(val_score - test_score) / max(abs(val_score), 1e-9)
        if test_score < self.policy.min_test_score:
            return self._reject(candidate, "weak_unseen_test")
        if gap > self.policy.max_validation_test_gap:
            return self._reject(candidate, "validation_test_gap")
        candidate.score = test_score
        candidate.stage = Stage.PROMOTED
        return candidate

    @staticmethod
    def _reject(candidate: Candidate, reason: str) -> Candidate:
        candidate.stage = Stage.REJECTED
        candidate.reasons.append(reason)
        return candidate

    def run(self, candidates: Iterable[Candidate], **evaluators) -> list[Candidate]:
        results = []
        for candidate in candidates:
            results.append(self.evaluate(candidate, **evaluators))
        return results
