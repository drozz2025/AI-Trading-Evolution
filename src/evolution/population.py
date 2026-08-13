"""Population lifecycle: birth, survival, retirement and reproduction."""
from __future__ import annotations

import random
from .models import Agent, AgentStatus


def create_initial_population(size: int = 10, capital: float = 50.0, seed: int = 7) -> list[Agent]:
    rng = random.Random(seed)
    agents: list[Agent] = []
    for i in range(1, size + 1):
        agents.append(Agent(
            agent_id=f"AGENT-{i:04d}",
            initial_capital=capital,
            balance=capital,
            role="research_trader",
            status=AgentStatus.BORN,
            metadata={
                "research_seed": rng.randrange(1_000_000),
                "risk_budget": rng.uniform(0.10, 1.00),
            },
        ))
    return agents


def retire_broke_agents(agents: list[Agent]) -> list[Agent]:
    for agent in agents:
        if agent.balance <= 0 and agent.status != AgentStatus.RETIRED:
            agent.balance = 0.0
            agent.status = AgentStatus.RETIRED
    return agents


def rank_survivors(agents: list[Agent], keep: int) -> list[Agent]:
    """Select by research score while penalising excessive drawdown."""
    alive = [a for a in agents if a.alive]
    return sorted(alive, key=lambda a: a.score - 1.5 * a.max_drawdown, reverse=True)[:max(1, keep)]


def reproduce(survivors: list[Agent], next_id: int, children_per_parent: int = 1, seed: int = 7) -> list[Agent]:
    """Create fresh €50 descendants with inherited but mutated research settings."""
    rng = random.Random(seed + next_id)
    children: list[Agent] = []
    for parent in survivors:
        for _ in range(children_per_parent):
            risk = float(parent.metadata.get("risk_budget", 0.5))
            child = Agent(
                agent_id=f"AGENT-{next_id:04d}",
                parent_id=parent.agent_id,
                role=parent.role,
                status=AgentStatus.BORN,
                initial_capital=50.0,
                balance=50.0,
                generation=parent.generation + 1,
                metadata={
                    **parent.metadata,
                    "research_seed": rng.randrange(1_000_000),
                    "risk_budget": max(0.10, min(1.00, risk * rng.uniform(0.85, 1.15))),
                },
            )
            children.append(child)
            next_id += 1
    return children


def population_summary(agents: list[Agent]) -> dict:
    return {
        "total": len(agents),
        "alive": sum(a.alive for a in agents),
        "retired": sum(a.status == AgentStatus.RETIRED for a in agents),
        "capital": round(sum(a.balance for a in agents), 2),
        "generations": max((a.generation for a in agents), default=0),
        "promoted": sum(a.status == AgentStatus.PROMOTED for a in agents),
        "researching": sum(a.status == AgentStatus.RESEARCHING for a in agents),
        "backtesting": sum(a.status == AgentStatus.BACKTESTING for a in agents),
        "validating": sum(a.status == AgentStatus.VALIDATING for a in agents),
        "arena": sum(a.status == AgentStatus.ARENA for a in agents),
    }
