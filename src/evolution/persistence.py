from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

STATE_PATH = Path('data/viveiro_state.json')

DEFAULT_STATE: dict[str, Any] = {
    'mode': 'LAB', 'generation': 0, 'capital': 1000.0,
    'agents': [], 'strategies': [], 'backtests': [], 'tasks': [], 'history': [],
    'live_trading_enabled': False,
}

def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    if not path.exists():
        return dict(DEFAULT_STATE)
    with path.open('r', encoding='utf-8') as f:
        state = json.load(f)
    return {**DEFAULT_STATE, **state}

def save_state(state: dict[str, Any], path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state['updated_at'] = datetime.now(timezone.utc).isoformat()
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    tmp.replace(path)

def append_event(state: dict[str, Any], kind: str, payload: dict[str, Any]) -> None:
    state.setdefault('history', []).append({'at': datetime.now(timezone.utc).isoformat(), 'kind': kind, **payload})
    state['history'] = state['history'][-2000:]
