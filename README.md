# AI Trading Evolution

An experimental multi-agent trading research platform for XAUUSD.

## Mission

Build a controlled artificial trading organization in which agents research markets, develop and test their own strategies, cooperate or compete, evolve, reproduce, and are promoted or retired according to measurable performance.

## Safety boundary

The initial system is **simulation-only**. Agents start with virtual capital and cannot place live orders. Real/demo execution will be isolated behind explicit controls and added only after robust out-of-sample validation.

## Planned organization

- **Master AI** — coordinates research priorities and capital allocation.
- **Trading Directorate** — manages trading teams and strategy deployment.
- **Research Directorate** — discovers hypotheses, features, factors and strategies.
- **Risk Directorate** — monitors drawdown, exposure, correlation and failure conditions.
- **Agents** — autonomous research/trading entities with virtual capital, memory and lineage.
- **Arena** — standardized evaluation environment using historical and unseen market data.
- **Evolution Engine** — selection, mutation, recombination, reproduction and retirement.
- **Dashboard** — hierarchy, population, capital, performance, strategies, lineage and system health.

## Initial population

The first milestone targets 10 simulated agents with €50 virtual starting capital each. This is a research parameter, not a promise of profitability.

## Principles

1. No look-ahead bias.
2. Strict train/validation/test separation.
3. Walk-forward evaluation.
4. Transaction costs and slippage included.
5. Anti-overfitting tests before promotion.
6. Every strategy has provenance and version history.
7. Every agent has a measurable lineage and lifecycle state.
8. Live trading is disabled by default.

## Roadmap

- [ ] Core domain model and agent lifecycle
- [ ] Market-data abstraction
- [ ] Backtesting engine
- [ ] Strategy research/evolution engine
- [ ] Arena and scoring
- [ ] Hierarchy and governance
- [ ] Dashboard
- [ ] MT5 paper/demo adapter
- [ ] Production risk controls
