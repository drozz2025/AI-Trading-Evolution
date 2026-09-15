"""Download real daily OHLC data from Stooq public CSV endpoint for laboratory backtests."""
from pathlib import Path
from urllib.request import Request,urlopen
SYMBOLS={'EURUSD':'eurusd','XAUUSD':'xauusd','GBPUSD':'gbpusd','USDJPY':'usdjpy'}
OUT=Path('data/market');OUT.mkdir(parents=True,exist_ok=True)
for name,sym in SYMBOLS.items():
    url=f'https://stooq.com/q/d/l/?s={sym}&d1=20180101&i=d'
    try:
        req=Request(url,headers={'User-Agent':'Mozilla/5.0 AI-Trading-Evolution-Lab'})
        raw=urlopen(req,timeout=30).read().decode('utf-8')
        if 'Open' not in raw or raw.count('\n')<100: raise RuntimeError('insufficient response')
        (OUT/f'{name}_D1.csv').write_text(raw,encoding='utf-8')
        print(name,'OK',raw.count('\n')-1,'bars')
    except Exception as e: print(name,'FAILED',e)
