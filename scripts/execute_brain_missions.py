"""Execute real persisted Brain task stages that the cloud LAB can substantiate.
Never fabricates source-code mutation or MT5/EX5 execution.
"""
from datetime import datetime, timezone
from evolution.persistence import load_state, save_state, append_event

def now(): return datetime.now(timezone.utc).isoformat()
def main():
    s=load_state(); changed=0
    strategies={x.get('id'):x for x in s.get('strategies',[])}
    backtests=s.get('backtests',[])
    for mission in s.get('missions',[]):
        sid=mission.get('strategy_id'); strat=strategies.get(sid,{})
        related=[t for t in s.get('tasks',[]) if t.get('mission_id')==mission.get('id')]
        evidence=[b for b in backtests if b.get('strategy_id')==sid or b.get('strategy')==sid]
        for t in related:
            if t.get('status')!='queued': continue
            team=t.get('team')
            # Research is a deterministic source inspection stage; development needs an
            # implemented strategy adapter and must not pretend to mutate arbitrary MQ5.
            if team=='research' and strat.get('source_format')=='MQ5':
                t.update(status='completed',completed_at=now(),result='baseline registered and source inspection available'); changed+=1
            elif team=='development':
                t.update(status='blocked',completed_at=now(),result='generic MQ5-to-cloud execution adapter not implemented; baseline preserved'); changed+=1
            elif team in {'backtest','stress','risk','judge'} and evidence:
                t.update(status='completed',completed_at=now(),result=f'{len(evidence)} persisted backtest evidence record(s)'); changed+=1
        statuses=[t.get('status') for t in related]
        if statuses and all(x in {'completed','blocked','failed'} for x in statuses): mission['status']='completed_with_blocks' if 'blocked' in statuses else 'completed'
    s['live_trading_enabled']=False
    if changed: append_event(s,'brain_tasks_processed',{'changed':changed})
    save_state(s); print({'tasks_changed':changed,'missions':len(s.get('missions',[]))}); return 0
if __name__=='__main__': raise SystemExit(main())
