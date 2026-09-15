from __future__ import annotations
from datetime import datetime, timezone
from evolution.persistence import load_state, save_state, append_event

def status():
    s=load_state()
    return {
      'mode':s['mode'],'generation':s['generation'],'capital':s['capital'],
      'agents':len(s['agents']),'strategies':len(s['strategies']),'backtests':len(s['backtests']),
      'tasks':s['tasks'][-50:],'live_trading_enabled':False,'updated_at':s.get('updated_at')
    }

def queue_task(agent_id:str, task_type:str, detail:str=''):
    s=load_state(); t={'id':f"TASK-{len(s['tasks'])+1:05d}",'agent_id':agent_id,'type':task_type,'detail':detail,'status':'queued','created_at':datetime.now(timezone.utc).isoformat()}
    s['tasks'].append(t); append_event(s,'task_queued',t); save_state(s); return t

def record_strategy(name:str, parent_ids=None):
    s=load_state(); item={'id':f"STRAT-{len(s['strategies'])+1:05d}",'name':name,'generation':s['generation'],'parents':parent_ids or [],'stage':'research'}
    s['strategies'].append(item); append_event(s,'strategy_created',item); save_state(s); return item

def record_backtest(strategy_id:str, metrics:dict):
    s=load_state(); item={'id':f"BT-{len(s['backtests'])+1:06d}",'strategy_id':strategy_id,'metrics':metrics,'stage':'completed'}
    s['backtests'].append(item); append_event(s,'backtest_completed',item); save_state(s); return item

def promote_generation(survivors:list[str]):
    s=load_state(); s['generation']+=1; append_event(s,'generation_promoted',{'generation':s['generation'],'survivors':survivors}); save_state(s); return s['generation']
