from .models import Agent, AgentStatus


def create_initial_population(size: int = 10, capital: float = 50.0) -> list[Agent]:
    return [
        Agent(agent_id=f"AGENT-{i:03d}", initial_capital=capital, balance=capital)
        for i in range(1, size + 1)
    ]


def retire_broke_agents(agents: list[Agent]) -> list[Agent]:
    for agent in agents:
        if agent.balance <= 0 and agent.status != AgentStatus.RETIRED:
            agent.balance = 0.0
            agent.status = AgentStatus.RETIRED
    return agents


def population_summary(agents: list[Agent]) -> dict:
    return {
        "total": len(agents),
        "alive": sum(a.alive for a in agents),
        "retired": sum(a.status == AgentStatus.RETIRED for a in agents),
        "capital": round(sum(a.balance for a in agents), 2),
        "generations": max((a.generation for a in agents), default=0),
    }
