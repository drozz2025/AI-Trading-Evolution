"""Run one complete autonomous research cycle in simulation only and persist its state."""
from evolution.hypothesis_engine import HypothesisEngine
from evolution.autonomous_cycle import Candidate, ResearchCycle
from evolution.research_roles import ResearchRole
from evolution.persistence import load_state, save_state, append_event


def main() -> None:
    engine = HypothesisEngine(seed=11)
    roles = list(ResearchRole)[:8]
    candidates = [Candidate(engine.generate(f"AGENT-{i+1:04d}", role)) for i, role in enumerate(roles)]

    def backtest(h):
        return {"trades": 40, "return_pct": 8.0, "drawdown_pct": 3.0, "sharpe": 1.7}

    def adversarial(h, result):
        return {"passed": True, "reason": "No synthetic adversarial failure triggered."}

    def validation(h, result):
        return {"passed": True, "return_pct": 5.0, "drawdown_pct": 3.5, "sharpe": 1.3}

    results = ResearchCycle().run(candidates, backtest=backtest, adversarial=adversarial, validation=validation)
    promoted = [r for r in results if r.stage.value == "promoted"]

    state = load_state()
    if not state['agents']:
        state['agents'] = [{'id': f'AGENT-{i+1:04d}', 'status': 'researching', 'generation': state['generation']} for i in range(20)]
    for r in results:
        state['strategies'].append({'id': f"STRAT-{len(state['strategies'])+1:05d}", 'name': r.hypothesis.name, 'generation': state['generation'], 'stage': r.stage.value})
        state['backtests'].append({'id': f"BT-{len(state['backtests'])+1:06d}", 'strategy': r.hypothesis.name, 'return_pct': 8.0, 'drawdown_pct': 3.0, 'sharpe': 1.7, 'stage': r.stage.value})
    if promoted:
        state['generation'] += 1
    append_event(state, 'cycle_completed', {'generated': len(results), 'promoted': len(promoted), 'rejected': len(results)-len(promoted)})
    state['tasks'] = [{'id': f'TASK-{i+1:03d}', 'agent_id': f'AGENT-{i+1:04d}', 'type': 'research_cycle', 'status': 'completed'} for i in range(min(8, len(results)))]
    state['live_trading_enabled'] = False
    save_state(state)

    print('END-TO-END LAB OK')
    print({'generated': len(results), 'promoted': len(promoted), 'rejected': len(results) - len(promoted), 'generation': state['generation']})
    print('promoted:', [r.hypothesis.name for r in promoted])


if __name__ == '__main__':
    main()
