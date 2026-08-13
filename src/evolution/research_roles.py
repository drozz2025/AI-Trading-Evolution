"""Research specializations used to diversify the agent population."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ResearchRole(str, Enum):
    PRICE_ACTION = "price_action"
    MARKET_STRUCTURE = "market_structure"
    VOLATILITY = "volatility"
    REGIME = "regime"
    ORDER_FLOW = "order_flow"
    MEAN_REVERSION = "mean_reversion"
    MOMENTUM = "momentum"
    CROSS_ASSET = "cross_asset"
    EVENT_DRIVEN = "event_driven"
    ADVERSARIAL = "adversarial"
    ENSEMBLE = "ensemble"


@dataclass(frozen=True)
class ResearchMandate:
    role: ResearchRole
    objective: str
    allowed_features: tuple[str, ...]
    forbidden_shortcut: str


MANDATES: dict[ResearchRole, ResearchMandate] = {
    ResearchRole.PRICE_ACTION: ResearchMandate(ResearchRole.PRICE_ACTION, "discover repeatable candle and swing behaviour", ("returns", "ranges", "swings"), "no single-indicator rules"),
    ResearchRole.MARKET_STRUCTURE: ResearchMandate(ResearchRole.MARKET_STRUCTURE, "model breaks, trends and structural transitions", ("swings", "breaks", "levels"), "no fixed RSI thresholds"),
    ResearchRole.VOLATILITY: ResearchMandate(ResearchRole.VOLATILITY, "adapt entries and exits to changing volatility", ("true_range", "realized_vol", "range"), "no static stop distance"),
    ResearchRole.REGIME: ResearchMandate(ResearchRole.REGIME, "detect latent market regimes and switch behaviour", ("returns", "volatility", "trend_state"), "no look-ahead regime labels"),
    ResearchRole.ORDER_FLOW: ResearchMandate(ResearchRole.ORDER_FLOW, "test microstructure and volume proxies when available", ("volume", "spread", "imbalance"), "no future-bar information"),
    ResearchRole.MEAN_REVERSION: ResearchMandate(ResearchRole.MEAN_REVERSION, "find statistically persistent dislocations", ("zscore", "distance", "half_life"), "no arbitrary overbought/oversold levels"),
    ResearchRole.MOMENTUM: ResearchMandate(ResearchRole.MOMENTUM, "find persistence and acceleration effects", ("returns", "slope", "acceleration"), "no single moving-average crossover"),
    ResearchRole.CROSS_ASSET: ResearchMandate(ResearchRole.CROSS_ASSET, "test relationships with other liquid markets", ("correlation", "relative_strength", "lead_lag"), "no contemporaneous leakage"),
    ResearchRole.EVENT_DRIVEN: ResearchMandate(ResearchRole.EVENT_DRIVEN, "test behaviour around scheduled market events", ("event_time", "pre_event", "post_event"), "no using revised future information"),
    ResearchRole.ADVERSARIAL: ResearchMandate(ResearchRole.ADVERSARIAL, "try to falsify candidate strategies and expose fragility", ("drawdown", "regime", "slippage"), "never optimize only for headline return"),
    ResearchRole.ENSEMBLE: ResearchMandate(ResearchRole.ENSEMBLE, "combine weakly correlated candidates robustly", ("returns", "risk", "correlation"), "no averaging without out-of-sample evidence"),
}


def assign_roles(agent_ids: list[str]) -> dict[str, ResearchRole]:
    roles = list(ResearchRole)
    return {agent_id: roles[i % len(roles)] for i, agent_id in enumerate(agent_ids)}


def build_hypothesis(role: ResearchRole, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a testable hypothesis specification, not a trading signal."""
    mandate = MANDATES[role]
    context = context or {}
    return {
        "role": role.value,
        "objective": mandate.objective,
        "features": list(mandate.allowed_features),
        "constraint": mandate.forbidden_shortcut,
        "context": context,
        "requires_out_of_sample": True,
        "requires_cost_model": True,
    }
