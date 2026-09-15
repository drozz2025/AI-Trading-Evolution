"""Safe text-only MQ5 ingestion for the Viveiro LAB.
Does not compile or execute user code. Persistence is repository/filesystem-side.
"""
from __future__ import annotations
import hashlib, re
from pathlib import Path
from evolution.control_plane import ingest_baseline

INPUT_RE=re.compile(r'^\s*input\s+([\w<>]+)\s+(\w+)\s*=\s*([^;]+);',re.M)

def inspect_mq5(source:str)->dict:
    return {'inputs':[{'type':t,'name':n,'default':v.strip()} for t,n,v in INPUT_RE.findall(source)],'has_on_init':bool(re.search(r'\bOnInit\s*\(',source)),'has_on_tick':bool(re.search(r'\bOnTick\s*\(',source))}

def ingest_mq5_text(filename:str, source:str, root:Path|str='strategies/baselines')->dict:
    if not filename.lower().endswith('.mq5'): raise ValueError('MQ5 source required')
    if not source.strip(): raise ValueError('Empty MQ5 source')
    digest=hashlib.sha256(source.encode('utf-8')).hexdigest()
    safe=Path(filename).name
    out=Path(root); out.mkdir(parents=True,exist_ok=True)
    path=out/f'{digest[:12]}_{safe}'
    if not path.exists(): path.write_text(source,encoding='utf-8')
    result=ingest_baseline(safe,'MQ5',content_sha256=digest,source_path=str(path))
    result['inspection']=inspect_mq5(source); result['sha256']=digest
    return result
