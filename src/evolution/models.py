from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AgentStatus(str, Enum):
    BORN = "born"
    RESEARCHING = "researching"
    BACKTESTING = "backtesting"
    VALIDATING = "validating"
    ARENA = "arena"
    PROMOTED = "promoted"
    RETIRED = "retired"


@dataclass
class Agent:
    agent_id: str
    parent_id: Optional[str] = None
    role: str = "research_trader"
    status: AgentStatus = AgentStatus.BORN
    initial_capital: float = 50.0
    balance: float = 50.0
    strategy_id: Optional[str] = None
    generation: int = 0
    score: float = 0.0
    sharpe: float = 0.0
    max_drawdown: float = 0.0
    metadata: dict = field(default_factory=dict)

    @property
    def alive(self) -> bool:
        return self.status != AgentStatus.RETIRED and self.balance > 0


@dataclass
class Strategy:
    strategy_id: str
    creator_agent_id: str
    version: int = 1
    description: str = ""
    parameters: dict = field(default_factory=dict)
    parent_strategy_id: Optional[str] = None
    status: str = "candidate"
