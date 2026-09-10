import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
OUT = Path("bls-test/live-consensus.json")


def num(s):
    if s is None:
        return None
    s = s.strip().replace(",", "").replace("%", "")
    if not s or s == "-":
        return None
    mult = 1.0
    if s[-1:].upper() == "K":
        s = s[:-1]
    elif s[-1:].upper() == "M":
        s = s[:-1]
        mult = 1000.0
    elif s[-1:].upper() == "B":
        s = s[:-1]
        mult = 1000000.0
    m = re.search(r"[-+]?\d+(?:\.\d+)?", s)
    return None if not m else float(m.group(0)) * mult


def classify(title):
    t = title.lower()
    if "cpi" in t and ("y/y" in t or "yy" in t or "year" in t) and "core" not in t:
        return "CPI"
    if "non-farm" in t or "nonfarm" in t or "non farm" in t:
        return "NFP"
    return None


def parse_date(s):
    s = s.strip()
    for fmt in ("%m-%d-%Y", "%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return None

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=20) as r:
    xml = r.read()

root = ET.fromstring(xml)
events = []
for e in root.findall(".//event"):
    country = (e.findtext("country") or "").strip()
    title = (e.findtext("title") or "").strip()
    typ = classify(title)
    if country != "USD" or not typ:
        continue
    date = parse_date(e.findtext("date") or "")
    forecast = num(e.findtext("forecast"))
    previous = num(e.findtext("previous"))
    if not date or forecast is None:
        continue
    events.append({
        "currency": "USD",
        "type": typ,
        "title": title,
        "date": date,
        "forecast": forecast,
        "previous": previous,
    })

if not events:
    raise SystemExit("No CPI/NFP consensus events parsed; refusing to overwrite current feed")

payload = {
    "updated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "source": URL,
    "events": events,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2))
