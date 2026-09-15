"""Run one autonomous Viveiro generation against real historical OHLC data."""
from pathlib import Path
import random
from evolution.market_backtest import load_ohlc, walk_forward
from evolution.persistence import load_state, save_state, append_event

SEEDS=[(5,20),(8,30),(12,36),(15,50),(20,60),(24,72),(30,90),(40,120)]

def evaluate(rows,fast,slow):
    wf=walk_forward(rows,fast=fast,slow=slow,spread_bps=1,commission_bps=.5,slippage_bps=.5)
    train,test=wf['train'],wf['test']
    promoted=(train['trades']>=20 and train['max_drawdown']<=.20 and test['trades']>=5 and test['max_drawdown']<=.20 and test['score']>0)
    fitness=float(test['score'])-1.5*float(test['max_drawdown'])
    return train,test,promoted,fitness

def mutate(fast,slow,rng):
    nf=max(2,int(round(fast*rng.uniform(.80,1.20))))
    ns=max(nf+3,int(round(slow*rng.uniform(.80,1.20))))
    return nf,ns

def main():
    files=sorted(Path('data/market').glob('*.csv'))
    if not files:
        print('REAL MARKET LAB SKIPPED: no OHLC data'); return 2
    s=load_state(); generation=int(s.get('generation',0)); rng=random.Random(7000+generation)
    previous=[x for x in s.get('strategies',[]) if x.get('stage')=='promoted'][-4:]
    specs=[]
    if previous:
        for p in previous:
            par=p.get('parameters',{}); f=int(par.get('fast',8)); sl=int(par.get('slow',30))
            specs.append((f,sl,p.get('id'))); nf,ns=mutate(f,sl,rng); specs.append((nf,ns,p.get('id')))
    else: specs=[(f,sl,None) for f,sl in SEEDS]
    candidates=[]
    # Evaluate every candidate across all downloaded markets, not only one file.
    for fast,slow,parent in specs:
        market_results=[]
        for file in files:
            rows=load_ohlc(file); train,test,ok,fitness=evaluate(rows,fast,slow)
            market_results.append({'source':file.name,'train':train,'test':test,'passed':ok,'fitness':fitness})
        passed=sum(r['passed'] for r in market_results); avg=sum(r['fitness'] for r in market_results)/len(market_results)
        promoted=passed>=max(1,(len(market_results)+1)//2) and avg>0
        sid=f"STRAT-{len(s['strategies'])+1:05d}"
        item={'id':sid,'name':f'SMA-{fast}-{slow}','generation':generation,'parent_strategy_id':parent,'parameters':{'fast':fast,'slow':slow},'stage':'promoted' if promoted else 'rejected','fitness':avg,'markets_passed':passed,'markets_total':len(market_results),'results':market_results}
        s['strategies'].append(item); candidates.append(item)
        for mr in market_results:
            s['backtests'].append({'id':f"BT-{len(s['backtests'])+1:06d}",'strategy':sid,'generation':generation,'source':mr['source'],'train':mr['train'],'test':mr['test'],'stage':'promoted' if mr['passed'] else 'rejected'})
    survivors=sorted((x for x in candidates if x['stage']=='promoted'),key=lambda x:x['fitness'],reverse=True)[:4]
    if survivors: s['generation']=generation+1
    # Persist an explicit population/lineage view for the dashboard.
    agents=[]
    for i,c in enumerate(candidates,1):
        agents.append({'id':f'AGENT-G{generation}-{i:03d}','generation':generation,'parent_strategy_id':c['parent_strategy_id'],'strategy_id':c['id'],'status':'promoted' if c in survivors else 'retired','score':c['fitness'],'balance':50.0 if c in survivors else 0.0})
    s['agents']=agents; s['capital']=round(sum(a['balance'] for a in agents),2)
    s['live_trading_enabled']=False
    append_event(s,'real_market_evolution',{'generation':generation,'datasets':[f.name for f in files],'tested':len(candidates),'promoted':len(survivors),'rejected':len(candidates)-len(survivors)})
    save_state(s); print({'generation':s['generation'],'tested':len(candidates),'promoted':len(survivors),'markets':len(files)}); return 0
if __name__=='__main__': raise SystemExit(main())
