"""High-level orchestration for the research company."""
from __future__ import annotations

from dataclasses import dataclass, field
from .agent_org import ResearchDirector
from .strategy_lab import ResearchGate, ResearchResult


@dataclass
class ResearchOrchestrator:
    director: ResearchDirector = field(default_factory=ResearchDirector)
    gate: ResearchGate = field(default_factory=ResearchGate)
    arena: list[ResearchResult] = field(default_factory=list)

    def bootstrap(self, count: int = 12) -> dict[str, object]:
        self.director.seed(count)
        return self.snapshot()

    def submit(self, result: ResearchResult, agent_id: str) -> ResearchResult:
        evaluated = self.gate.evaluate(result)
        agent = next(a for a in self.director.agents if a.agent_id == agent_id)
        if evaluated.status == "PROMOTE":
            self.director.promote(agent)
            self.arena.append(evaluated)
        else:
            self.director.reject(agent)
        return evaluated

    def snapshot(self) -> dict[str, object]:
        return {
            "organization": self.director.snapshot(),
            "arena_size": len(self.arena),
            "promoted_strategies": sum(1 for r in self.arena if r.status == "PROMOTE"),
        }
