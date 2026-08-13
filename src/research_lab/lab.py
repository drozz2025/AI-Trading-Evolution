"""First controlled laboratory: synthetic XAUUSD-like market + evolving agents.

No live trading, broker connection, or future-data access is used here.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random
from statistics import mean, pstdev


@dataclass(frozen=True)
class Genome:
    fast: int
    slow: int
    momentum: int
    threshold: float
    risk: float


@dataclass
class Result:
    return_pct: float
    sharpe: float
    max_drawdown: float
    trades: int
    score: float


def make_market(n: int = 3000, seed: int = 7) -> list[float]:
    """Generate a deterministic synthetic XAUUSD-like price series for smoke testing."""
    rng = random.Random(seed)
    price = 2000.0
    prices = [price]
    regime = 0.0
    for i in range(1, n):
        if i % 350 == 0:
            regime = rng.choice((-0.00035, 0.0, 0.00035))
        cyclical = 0.00045 * math.sin(i / 47.0) + 0.00025 * math.sin(i / 113.0)
        shock = rng.gauss(0.0, 0.0014)
        price *= math.exp(regime + cyclical + shock)
        prices.append(price)
    return prices


def _mean(values: list[float]) -> float:
    return mean(values) if values else 0.0


def _signal(prices: list[float], i: int, g: Genome) -> int:
    fast = _mean(prices[i-g.fast+1:i+1])
    slow = _mean(prices[i-g.slow+1:i+1])
    momentum = prices[i] / prices[i-g.momentum] - 1.0
    spread = (fast / slow) - 1.0
    if spread > g.threshold and momentum > 0:
        return 1
    if spread < -g.threshold and momentum < 0:
        return -1
    return 0


def evaluate(prices: list[float], g: Genome, start: int, end: int, fee_bps: float = 2.0) -> Result:
    """Evaluate only the requested window; signals use data available before each bar."""
    warmup = max(g.slow, g.momentum) + 1
    first = max(start, warmup)
    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    returns: list[float] = []
    position = 0
    trades = 0
    for i in range(first, end):
        new_position = _signal(prices, i - 1, g)
        changed = new_position != position
        if changed:
            trades += int(new_position != 0)
        market_return = prices[i] / prices[i - 1] - 1.0
        pnl = new_position * market_return * g.risk
        if changed and new_position != 0:
            pnl -= fee_bps / 10000.0
        position = new_position
        equity *= max(0.0001, 1.0 + pnl)
        returns.append(pnl)
        peak = max(peak, equity)
        max_dd = max(max_dd, 1.0 - equity / peak)
    avg = _mean(returns)
    vol = pstdev(returns) if len(returns) > 1 else 0.0
    sharpe = (avg / vol) * math.sqrt(252) if vol else 0.0
    score = math.log(max(equity, 1e-12)) + 0.35 * sharpe - 1.5 * max_dd
    return Result((equity - 1.0) * 100, sharpe, max_dd * 100, trades, score)


def mutate(g: Genome, rng: random.Random) -> Genome:
    """Small bounded mutation: the evolutionary engine can search, not memorize."""
    return Genome(
        fast=max(3, min(80, g.fast + rng.randint(-5, 5))),
        slow=max(10, min(240, g.slow + rng.randint(-15, 15))),
        momentum=max(2, min(80, g.momentum + rng.randint(-5, 5))),
        threshold=max(0.00005, min(0.01, g.threshold * rng.uniform(0.75, 1.25))),
        risk=max(0.10, min(1.0, g.risk * rng.uniform(0.85, 1.15))),
    )


def run(seed: int = 7, population: int = 10, generations: int = 5) -> dict:
    """Run a small lab evolution with strict train/validation/test separation."""
    prices = make_market(seed=seed)
    train_end = int(len(prices) * 0.60)
    valid_end = int(len(prices) * 0.80)
    rng = random.Random(seed)
    agents = [
        Genome(rng.randint(5, 40), rng.randint(50, 160), rng.randint(3, 35), rng.uniform(0.0001, 0.002), rng.uniform(0.25, 1.0))
        for _ in range(population)
    ]
    for _ in range(generations):
        scored = [(evaluate(prices, g, 0, train_end), g) for g in agents]
        scored.sort(key=lambda x: x[0].score, reverse=True)
        parents = [g for _, g in scored[:max(2, population // 3)]]
        agents = parents + [mutate(rng.choice(parents), rng) for _ in range(population - len(parents))]
    final = [(evaluate(prices, g, 0, train_end), g) for g in agents]
    final.sort(key=lambda x: x[0].score, reverse=True)
    best = final[0][1]
    validation = evaluate(prices, best, train_end, valid_end)
    test = evaluate(prices, best, valid_end, len(prices))
    return {"best_genome": best, "validation": validation, "test": test, "population": population, "generations": generations}
