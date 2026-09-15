"""THE BRAIN: persisted LAB-only strategy mission orchestrator."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable
from .persistence import load_state, save_state, append_event

TEAM_PLAN = (
    ("research",4,"analyse baseline, weaknesses and improvement hypotheses"),
    ("development",5,"create isolated descendants; never modify baseline"),
    ("backtest",4,"run identical in/out-of-sample and walk-forward tests"),
    ("stress",2,"attack robustness with adverse assumptions"),
    ("risk",3,"measure drawdown, stability, exposure and overfitting"),
    ("judge",2,"rank candidates and recommend promotion/rejection"),
)
BENCHMARK_PLAN = (
    ("backtest",4,"benchmark closed EX5 after external MT5 result import"),
    ("stress",2,"stress imported benchmark metrics"),
    ("risk",3,"audit imported benchmark risk"),
    ("judge",2,"judge benchmark without source mutation"),
)
@dataclass(frozen=True)
class Mission:
    id:str; strategy_id:str; baseline_name:str; created_at:str; status:str="queued"; mode:str="LAB"

def _active_agents(state): return [a for a in state.get('agents',[]) if str(a.get('status','')).lower()!='retired']

def create_strategy_mission(strategy_id:str, baseline_name:str, agents:Iterable[dict]|None=None, benchmark_only:bool=False)->dict:
    s=load_state(); pool=list(agents) if agents is not None else _active_agents(s)
    mission=Mission(f"MISSION-{len(s.get('missions',[]))+1:05d}",strategy_id,baseline_name,datetime.now(timezone.utc).isoformat())
    md=asdict(mission); md['benchmark_only']=benchmark_only; s.setdefault('missions',[]).append(md)
    plan=BENCHMARK_PLAN if benchmark_only else TEAM_PLAN; tasks=[]; cursor=0
    for team,requested,objective in plan:
        for _ in range(requested):
            if not pool: break
            agent=pool[cursor%len(pool)]; cursor+=1; aid=agent.get('agent_id') or agent.get('id') or f"AGENT-{cursor:04d}"
            task={'id':f"TASK-{len(s.setdefault('tasks',[]))+1:05d}",'mission_id':mission.id,'strategy_id':strategy_id,'agent_id':aid,'team':team,'type':objective,'status':'queued','created_at':mission.created_at}
            s['tasks'].append(task); tasks.append(task)
    append_event(s,'brain_mission_created',{'mission_id':mission.id,'strategy_id':strategy_id,'baseline':baseline_name,'benchmark_only':benchmark_only,'tasks':len(tasks)})
    s['live_trading_enabled']=False; save_state(s)
    return {'mission':md,'tasks':tasks,'teams':plan}

def team_summary(state=None):
    s=state or load_state(); out={k:{'queued':0,'running':0,'completed':0,'failed':0} for k,_,_ in TEAM_PLAN}
    for t in s.get('tasks',[]):
        team=t.get('team'); st=t.get('status','queued')
        if team in out: out[team][st]=out[team].get(st,0)+1
    return out

def promote_only_after_gates(candidate:dict,gates:dict)->bool:
    required=('backtest_pass','walk_forward_pass','stress_pass','risk_pass','judge_pass')
    return all(bool(gates.get(k)) for k in required) and candidate.get('baseline') is not True and candidate.get('benchmark_only') is not True
