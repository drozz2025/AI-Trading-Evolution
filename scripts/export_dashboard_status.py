"""Export persisted Viveiro state as frontend-safe JSON."""
import json
from pathlib import Path
from evolution.persistence import load_state
s=load_state(); agents=s.get('agents',[]); strategies=s.get('strategies',[]); backtests=s.get('backtests',[]); history=s.get('history',[])
promoted=[x for x in strategies if x.get('stage')=='promoted']; rejected=[x for x in strategies if x.get('stage')=='rejected']
best=sorted(strategies,key=lambda x:float(x.get('fitness',-999)),reverse=True)[:8]
gens={}
for x in strategies:
 g=str(x.get('generation',0)); gens.setdefault(g,{'generation':int(g),'tested':0,'promoted':0}); gens[g]['tested']+=1; gens[g]['promoted']+=x.get('stage')=='promoted'
payload={
 'mode':s.get('mode','LAB'),'generation':s.get('generation',0),'capital':s.get('capital',0),
 'agents':len(agents),'strategies':len(strategies),'backtests':len(backtests),
 'active_agents':sum(1 for a in agents if a.get('status')!='retired'),
 'promoted':len(promoted),'rejected':len(rejected),'promotion_rate':round(100*len(promoted)/max(1,len(strategies)),1),
 'best_strategies':best,'generation_stats':sorted(gens.values(),key=lambda x:x['generation'])[-20:],
 'agent_items':agents[-100:],'strategy_items':strategies[-100:],'backtest_items':backtests[-200:],
 'tasks':s.get('tasks',[])[-30:],'history':history[-100:],
 'live_trading_enabled':False,'updated_at':s.get('updated_at')
}
out=Path('dashboard/viveiro_status.json');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8');print(out)
