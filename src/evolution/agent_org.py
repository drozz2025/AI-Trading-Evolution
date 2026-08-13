"""Hierarchical organization for research agents."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .research_roles import RESEARCH_ROLES
from .strategy_lab import StrategyHypothesis


@dataclass
class ResearchAgent:
    agent_id: str
    role: str
    generation: int = 0
    parent_id: str | None = None
    capital: float = 50.0
    hypotheses_created: int = 0
    promoted: int = 0
    rejected: int = 0
    status: str = "RESEARCHING"

    def propose(self, thesis: str, features: Iterable[str], entry: str, exit: str, risk: str, timeframe: str, parameters: dict[str, float] | None = None) -> StrategyHypothesis:
        self.hypotheses_created += 1
        return StrategyHypothesis(
            name=f"{self.role}-{self.agent_id}-H{self.hypotheses_created:03d}",
            role=self.role,
            thesis=thesis,
            features=tuple(features),
            entry_logic=entry,
            exit_logic=exit,
            risk_logic=risk,
            timeframe=timeframe,
            parameters=parameters or {},
        )


@dataclass
class ResearchDirector:
    """Allocates research capacity and keeps role diversity."""
    agents: list[ResearchAgent] = field(default_factory=list)

    def seed(self, count: int = 12) -> list[ResearchAgent]:
        roles = list(RESEARCH_ROLES)
        for i in range(count):
            role = roles[i % len(roles)]
            self.agents.append(ResearchAgent(agent_id=f"R-{i+1:04d}", role=role))
        return self.agents

    def by_role(self, role: str) -> list[ResearchAgent]:
        return [a for a in self.agents if a.role == role]

    def promote(self, agent: ResearchAgent) -> None:
        agent.promoted += 1
        agent.status = "PROMOTED"

    def reject(self, agent: ResearchAgent) -> None:
        agent.rejected += 1
        agent.status = "RESEARCHING"

    def snapshot(self) -> dict[str, object]:
        return {
            "total_agents": len(self.agents),
            "roles": {role: len(self.by_role(role)) for role in RESEARCH_ROLES},
            "promoted": sum(a.promoted for a in self.agents),
            "hypotheses": sum(a.hypotheses_created for a in self.agents),
        }
