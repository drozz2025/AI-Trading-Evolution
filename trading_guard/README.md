# Trading Guard

A mobile-first trading risk and behaviour companion for beginner traders.

## MVP boundary

- MT5 cloud connection
- Read-only monitoring
- Account/equity/position data
- Deterministic risk rules
- Alerts and behavioural statistics
- Mobile dashboard

No live order execution is enabled in the MVP.

## Architecture

`Mobile -> Backend API -> MT5 cloud integration -> Broker/MT5`

## Development status

Backend foundation and initial risk engine are implemented. MT5 provider integration, authentication, persistence, mobile implementation, behaviour engine, alerts, subscriptions, security hardening and CI remain next milestones.
