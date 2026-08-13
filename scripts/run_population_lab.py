from evolution.population import create_initial_population, population_summary, rank_survivors, reproduce, retire_broke_agents


def main() -> None:
    agents = create_initial_population(size=12, capital=50.0, seed=7)
    for i, agent in enumerate(agents):
        agent.score = 0.5 + i * 0.1
        agent.max_drawdown = 0.01 * (i % 4)
        agent.status = agent.status.RESEARCHING
    retire_broke_agents(agents)
    survivors = rank_survivors(agents, keep=4)
    children = reproduce(survivors, next_id=13, children_per_parent=2, seed=7)
    all_agents = agents + children
    print("POPULATION LAB OK")
    print(population_summary(all_agents))
    print("survivors:", [a.agent_id for a in survivors])
    print("children:", [a.agent_id for a in children])


if __name__ == "__main__":
    main()
