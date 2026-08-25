from dataclasses import dataclass

@dataclass(frozen=True)
class BehaviourSignal:
    code: str
    severity: str
    message: str

def detect_behaviour(trades_today: int, consecutive_losses: int, current_volume: float, previous_volume: float | None) -> list[BehaviourSignal]:
    signals: list[BehaviourSignal] = []
    if consecutive_losses >= 2:
        signals.append(BehaviourSignal("revenge_risk", "high", "Multiple consecutive losses detected."))
    if previous_volume and current_volume > previous_volume * 1.5:
        signals.append(BehaviourSignal("size_jump", "medium", "Position size increased sharply versus the previous trade."))
    if trades_today >= 5:
        signals.append(BehaviourSignal("overtrading_risk", "medium", "Trade frequency is elevated."))
    return signals
