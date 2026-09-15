"""Run the Viveiro against a real historical OHLC CSV when available."""
from pathlib import Path
from evolution.market_backtest import load_ohlc, walk_forward
from evolution.persistence import load_state,save_state,append_event

def main():
    files=sorted(Path('data/market').glob('*.csv'))
    if not files:
        print('REAL MARKET LAB SKIPPED: add OHLC CSV under data/market/'); return 2
    rows=load_ohlc(files[-1]); s=load_state(); candidates=[]
    for fast,slow in [(5,20),(8,30),(12,36),(15,50),(20,60),(24,72),(30,90),(40,120)]:
        wf=walk_forward(rows,fast=fast,slow=slow,spread_bps=1,commission_bps=.5,slippage_bps=.5); bt=wf['train']; test=wf['test']
        promoted=bt['trades']>=20 and bt['max_drawdown']<=.20 and test['trades']>=5 and test['max_drawdown']<=.20 and test['score']>0
        item={'id':f"STRAT-{len(s['strategies'])+1:05d}",'name':f'SMA-{fast}-{slow}','generation':s['generation'],'stage':'promoted' if promoted else 'rejected','train':bt,'test':test,'source':files[-1].name}
        s['strategies'].append(item);s['backtests'].append({'id':f"BT-{len(s['backtests'])+1:06d}",'strategy':item['id'],'source':files[-1].name,'train':bt,'test':test,'stage':item['stage']}); candidates.append(item)
    survivors=[x for x in candidates if x['stage']=='promoted']
    if survivors: s['generation']+=1
    append_event(s,'real_market_cycle',{'dataset':files[-1].name,'tested':len(candidates),'promoted':len(survivors),'rejected':len(candidates)-len(survivors)})
    save_state(s);print({'dataset':files[-1].name,'tested':len(candidates),'promoted':len(survivors),'generation':s['generation']});return 0
if __name__=='__main__': raise SystemExit(main())
