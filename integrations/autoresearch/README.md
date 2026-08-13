# AutoResearch Lab Integration

This directory defines the integration boundary for `dietmarwo/autoresearch-trading`.

## Why it is integrated this way

The upstream project is MIT licensed and is designed around an autonomous LLM loop that proposes strategy code, runs walk-forward evaluation, keeps/reverts experiments, and feeds results back to the model. Its architecture separates AI strategy design from numerical parameter optimisation, which is useful for our research layer.

We intentionally keep the upstream project isolated rather than copying its source into the core engine. This lets us pin a known upstream revision, preserve attribution, and replace the research backend later without rewriting the agent/evolution system.

## Upstream

Repository: `https://github.com/dietmarwo/autoresearch-trading`
Pinned integration ref: `main` for the initial laboratory prototype.
License: MIT.

## Current boundary

```text
AI-Trading-Evolution
        |
        +-- agents / evolution / arena / risk
        |
        +-- AutoResearch Lab
                |
                +-- upstream strategy researcher
                +-- walk-forward evaluation
                +-- numerical parameter optimisation
                +-- experiment history
```

The AutoResearch Lab is research-only. It does not have permission to place MT5 orders.

## XAUUSD adaptation

The upstream runner is designed around OHLCV data and can work with different ticker sources. For our system, its strategy research contract will eventually be fed from our XAUUSD data adapter rather than allowing the research agent to decide its own live data source.

Before promotion to the Arena, every candidate must pass our independent validation gates. We do not use the upstream score as the sole promotion criterion.

## Local installation

From the repository root, create a Python virtual environment and run the platform bootstrap script. The bootstrap clones the upstream research component into `vendor/autoresearch-trading` at a pinned revision and installs its Python dependencies into the project environment.

Live execution remains disabled.
