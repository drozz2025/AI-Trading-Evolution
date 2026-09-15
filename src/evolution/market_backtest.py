"""OHLC backtest engine for real historical market files. No broker/live connectivity."""
from __future__ import annotations
import csv, math
from pathlib import Path

def load_ohlc(path:str|Path):
    rows=[]
    with open(path,newline='',encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            m={k.lower():v for k,v in r.items()}
            try: rows.append({k:float(m[k]) for k in ('open','high','low','close')})
            except (KeyError,ValueError,TypeError): continue
    if len(rows)<100: raise ValueError('historical dataset requires at least 100 valid OHLC bars')
    return rows

def sma(xs,n,i): return sum(xs[i-n+1:i+1])/n

def run_sma_cross(rows, fast=12, slow=36, spread_bps=1.0, commission_bps=0.5, slippage_bps=0.5):
    closes=[r['close'] for r in rows]; equity=1.0; peak=1.0; maxdd=0.0; trades=[]; pos=0; entry=0.0
    cost=(spread_bps+commission_bps+slippage_bps)/10000.0
    for i in range(slow,len(rows)):
        sig=1 if sma(closes,fast,i)>sma(closes,slow,i) else -1
        if pos and sig!=pos:
            raw=pos*(closes[i]/entry-1.0); net=raw-cost; equity*=max(0.000001,1+net); trades.append(net); peak=max(peak,equity); maxdd=max(maxdd,1-equity/peak); pos=0
        if not pos: pos=sig; entry=closes[i]
    if pos:
        net=pos*(closes[-1]/entry-1.0)-cost; equity*=max(0.000001,1+net); trades.append(net); peak=max(peak,equity); maxdd=max(maxdd,1-equity/peak)
    avg=sum(trades)/len(trades) if trades else 0; sd=math.sqrt(sum((x-avg)**2 for x in trades)/max(1,len(trades)-1)) if len(trades)>1 else 0
    score=(avg/sd*math.sqrt(len(trades))) if sd else 0
    return {'trades':len(trades),'return_pct':(equity-1)*100,'max_drawdown':maxdd,'max_drawdown_pct':maxdd*100,'score':score,'win_rate':sum(x>0 for x in trades)/len(trades) if trades else 0}

def walk_forward(rows, **kw):
    cut=max(70,int(len(rows)*.7)); train=run_sma_cross(rows[:cut],**kw); test=run_sma_cross(rows[cut-40:],**kw)
    return {'train':train,'test':test,'score':train['score'],'test_score':test['score']}
