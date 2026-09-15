"""Export persisted Viveiro state as frontend-safe JSON."""
import json
from pathlib import Path
from evolution.persistence import load_state
s=load_state()
payload={
 'mode':s['mode'],'generation':s['generation'],'capital':s['capital'],
 'agents':len(s['agents']),'strategies':len(s['strategies']),'backtests':len(s['backtests']),
 'active_agents':sum(1 for a in s['agents'] if a.get('status')!='retired'),
 'strategy_items':s['strategies'][-100:],'backtest_items':s['backtests'][-100:],
 'tasks':s['tasks'][-30:],'history':s['history'][-50:],
 'live_trading_enabled':False,'updated_at':s.get('updated_at')
}
out=Path('dashboard/viveiro_status.json');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8');print(out)
