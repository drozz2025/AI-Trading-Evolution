"""Refresh public OHLC history used by the Viveiro cloud laboratory.

Downloads complete history on every cycle so corrections and the newest completed
bar are picked up automatically.  Data is validated and written atomically: a
provider failure never destroys the last known-good history.
"""
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import json

SYMBOLS = {'EURUSD':'eurusd','XAUUSD':'xauusd','GBPUSD':'gbpusd','USDJPY':'usdjpy'}
OUT = Path('data/market')
OUT.mkdir(parents=True, exist_ok=True)
STATUS = OUT / 'history_status.json'
status = {'updated_at': datetime.now(timezone.utc).isoformat(), 'symbols': {}}

for name, sym in SYMBOLS.items():
    url = f'https://stooq.com/q/d/l/?s={sym}&d1=20000101&i=d'
    target = OUT / f'{name}_D1.csv'
    tmp = target.with_suffix('.tmp')
    try:
        req = Request(url, headers={'User-Agent':'Mozilla/5.0 AI-Trading-Evolution-Lab'})
        raw = urlopen(req, timeout=30).read().decode('utf-8')
        lines = [x for x in raw.splitlines() if x.strip()]
        if not lines or 'Date' not in lines[0] or 'Open' not in lines[0] or len(lines) < 100:
            raise RuntimeError('invalid or insufficient market history')
        tmp.write_text(raw, encoding='utf-8')
        tmp.replace(target)
        last = lines[-1].split(',')[0]
        status['symbols'][name] = {'ok': True, 'bars': len(lines)-1, 'last_bar': last, 'file': str(target)}
        print(name, 'OK', len(lines)-1, 'bars', 'last', last)
    except Exception as exc:
        if tmp.exists(): tmp.unlink()
        status['symbols'][name] = {'ok': False, 'error': str(exc), 'kept_previous': target.exists()}
        print(name, 'FAILED', exc)

STATUS.write_text(json.dumps(status, indent=2), encoding='utf-8')
# XAUUSD is mandatory for the requested gold laboratory. Fail the cycle rather
# than pretending that the history is current when no usable gold file exists.
xau = status['symbols']['XAUUSD']
if not xau['ok'] and not (OUT / 'XAUUSD_D1.csv').exists():
    raise SystemExit('No usable XAUUSD history available')
