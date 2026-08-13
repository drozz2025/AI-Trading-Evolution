# System Architecture

## Organization

```text
                         MASTER AI
                            |
              +-------------+-------------+
              |                           |
       TRADING DIRECTOR              RISK DIRECTOR
              |                           |
        +-----+-----+               +-----+-----+
        |     |     |               |     |     |
      TEAM A TEAM B TEAM C        Risk-1 Risk-2 Risk-3
        |
        +-------------------+
                            |
                       RESEARCH LAB
                            |
              +-------------+-------------+
              |             |             |
          Discovery      Evolution     Validation
              |             |             |
              +-------------+-------------+
                            |
                           ARENA
                            |
                   Simulation / OOS tests
                            |
                     Promotion / Retirement
```

## Agent lifecycle

`BORN -> RESEARCHING -> BACKTESTING -> VALIDATING -> ARENA -> PROMOTED | RETIRED`

Agents may create descendants only after meeting configurable quality gates. A descendant inherits lineage metadata but does not inherit performance credit automatically.

## Capital model

Every initial agent receives a virtual account. Initial configuration: `€50` per agent. Capital is a simulation metric and must never be interpreted as a guaranteed path to live profitability.

## Learning model

Agents may generate hypotheses and candidate strategies. Candidate strategies are evaluated against data that the agent has not used for fitting. The evaluation pipeline must include transaction costs, slippage assumptions, walk-forward testing, regime segmentation and robustness/Monte Carlo analysis where appropriate.

## Collaboration

Agents can publish research artifacts to a shared research registry. Collaboration is optional and must be measurable: the system records which information, hypotheses or strategy components were shared and whether the collaboration improved out-of-sample results.

## Governance

The Master AI can allocate research budgets and nominate agents for promotion, but hard risk limits remain deterministic and cannot be overridden by language-model output.

## Dashboard requirements

The dashboard should expose:

- population count and lifecycle state;
- organization hierarchy;
- virtual capital and equity curves;
- P&L, drawdown, Sharpe, expectancy and trade statistics;
- strategy registry and versions;
- validation status;
- agent lineage / family tree;
- collaboration graph;
- research activity;
- arena leaderboard;
- risk alerts;
- experiment reproducibility metadata.

## Execution boundary

The first releases are simulation-only. Any future MT5 integration must be an isolated adapter with an explicit enable flag, hard risk limits and a separate paper/demo mode.