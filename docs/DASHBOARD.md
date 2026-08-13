# Dashboard Specification

The dashboard is the command center for the artificial trading organization.

## Executive view

- Total agents
- Alive / retired / validating / researching
- Total virtual equity
- Starting virtual equity
- Current simulated P&L
- Maximum drawdown
- Arena leaders
- Active experiments
- Risk alerts

## Organization

Interactive hierarchy from Master AI to directors, teams and agents. Selecting an agent opens its profile, current mandate, capital, performance, strategy versions and lineage.

## Agent profile

- ID and lifecycle state
- Parent / descendants
- Virtual balance and equity curve
- P&L and risk metrics
- Current strategy version
- Research hypotheses
- Recent decisions
- Collaboration partners
- Promotion/retirement events

## Evolution view

A family tree showing which agents were created from which parents and which strategy mutations/recombinations produced each descendant.

## Strategy laboratory

- Candidate strategies
- Backtest results
- Out-of-sample results
- Walk-forward results
- Robustness tests
- Current deployment status
- Version lineage

## Arena

Leaderboard ranked by a composite score emphasizing risk-adjusted out-of-sample performance, robustness, drawdown and stability rather than raw profit alone.

## Design rule

The dashboard is observational first. It must not provide a hidden path for an AI-generated decision to bypass risk controls or enable live trading.
