from dataclasses import dataclass

@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    reasons: list[str]


def assess(*, consecutive_losses: int, trades_today: int, current_volume: float, previous_volume: float, floating_loss_pct: float = 0.0) -> RiskAssessment:
    score = 0
    reasons: list[str] = []
    if consecutive_losses >= 3:
        score += 30
        reasons.append("3 ou mais perdas consecutivas")
    if consecutive_losses >= 5:
        score += 20
        reasons.append("sequência elevada de perdas")
    if trades_today >= 10:
        score += 20
        reasons.append("frequência elevada de trades")
    if previous_volume > 0 and current_volume >= previous_volume * 2:
        score += 25
        reasons.append("aumento de lote >= 2x")
    if floating_loss_pct >= 5:
        score += 20
        reasons.append("perda flutuante elevada")
    score = min(score, 100)
    level = "SAFE" if score < 25 else "CAUTION" if score < 50 else "HIGH" if score < 75 else "CRITICAL"
    return RiskAssessment(score, level, reasons)
